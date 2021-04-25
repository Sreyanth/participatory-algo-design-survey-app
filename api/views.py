from pathlib import Path

import pandas as pd
from django.shortcuts import (HttpResponse, HttpResponseRedirect, render,
                              reverse)
from django.views import View

from .regression_code import run_regression

from webapp.views import user_fails_access_check

import random

from webapp.models import MechTaskCustomModel, MechTaskCustomModelSample, MechTaskStudentSample, MechTaskSurveyEstimate


BASE_DIR = str(Path(__file__).resolve().parent)
DATASET = BASE_DIR + '/data/pisa2009.csv'
df = pd.read_csv(DATASET)
new_cols = df.columns


class CreateLinearRegressionView(View):
    def build_model(self, cols):
        use_cols = [col for x in cols for col in new_cols if x in col]
        df_use = df[use_cols]
        X = df_use
        y = df['readingScore'].rank(pct=True)

        return run_regression(X, y)

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponse(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if survey_response.model:
            # Already has a model, skip everything
            # Else, we will assign the questions again and again! BAD IDEA!

            return HttpResponse(reverse('mech_task_understand_model'))

        if not survey_response.user_group.can_change_attributes:
            survey_response.selected_attributes = 'all'
            survey_response.save()

        if survey_response.selected_attributes is None:
            cols = request.POST.get('selected_attributes')
            selected_attributes = [x.strip() for x in cols.split(',')]
            selected_attributes_string = ', '.join(selected_attributes)

            survey_response.user_selected_attributes = selected_attributes_string

            if survey_response.user_group.has_deception:
                all_attrs = [
                    'male',
                    'raceeth',
                    'preschool',
                    'expectBachelors',
                    'computerForSchoolwork',
                    'read30MinsADay',
                    'minutesPerWeekEnglish',
                    'studentsInEnglish',
                    'schoolHasLibrary',
                    'publicSchool',
                    'urban',
                    'schoolSize',
                    'motherHS',
                    'motherBachelors',
                    'motherWork',
                    'fatherHS',
                    'fatherBachelors',
                    'fatherWork',
                    'selfBornUS',
                    'motherBornUS',
                    'fatherBornUS',
                    'englishAtHome'
                ]

                # Select some number of attributes for deception
                number_of_attrs = 16

                if len(selected_attributes) == number_of_attrs:
                    number_of_attrs = 17

                selected_attributes = random.sample(
                    all_attrs, number_of_attrs)
                selected_attributes_string = ', '.join(selected_attributes)

            # Build the actual model now!
            result, df_pred = self.build_model(selected_attributes)

            df_pred = df_pred[df_pred['linearReg_pred'] > 0]
            df_pred = df_pred[df_pred['linearReg_pred'] <= 1]

            # Record the model
            model = MechTaskCustomModel()
            model.attributes = selected_attributes_string
            model.average_error = result['test_mae'][0] * 100
            model.save()

            # Save the thing into the survey response
            survey_response.selected_attributes = selected_attributes_string
            survey_response.model = model
            survey_response.save()

            # Select 20 random samples
            selected_rows = random.sample(list(df_pred.index), 20)
            for row in selected_rows:
                sample = df_pred.loc[row]
                student = MechTaskStudentSample.objects.filter(
                    index_in_dataframe=row)[0]
                real_score = sample['y_true'] * 100
                model_score = sample['linearReg_pred'] * 100

                custom_sample = MechTaskCustomModelSample()
                custom_sample.sample = student
                custom_sample.model = model
                custom_sample.real_score = real_score
                custom_sample.linear_regression_prediction = model_score

                custom_sample.save()

                # Assign this as a question to the user
                estimate = MechTaskSurveyEstimate()
                estimate.survey_response = survey_response
                estimate.sample = student
                estimate.custom_sample = custom_sample
                estimate.real_score = real_score
                estimate.model_estimate = model_score
                estimate.save()

        return HttpResponse(reverse('mech_task_understand_model'))
