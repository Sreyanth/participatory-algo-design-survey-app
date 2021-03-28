from pathlib import Path

import pandas as pd
from django.shortcuts import (HttpResponse, HttpResponseRedirect, render,
                              reverse)
from django.views import View

from .regression_code import run_regression

from webapp.views import user_fails_access_check


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

        if not survey_response.user_group.can_change_attributes:
            survey_response.selected_attributes = 'all'
            survey_response.save()

        if survey_response.selected_attributes is None:
            cols = request.POST.get('selected_attributes')
            survey_response.selected_attributes = cols
            survey_response.save()
            result, df_pred = self.build_model(cols.split(','))

            print(result['test_mae'])

        return HttpResponse(reverse('mech_task_understand_model'))
