import csv
from pathlib import Path

from django.shortcuts import (HttpResponse, HttpResponseRedirect, render,
                              reverse)
from django.views import View

from webapp.models import MechTaskStudentSample, MechTaskAlgorithm, MechTaskUserGroup

from collections import OrderedDict


class SetupMechTaskView(View):
    def import_student_samples(self):
        BASE_DIR = str(Path(__file__).resolve().parent)

        with open(BASE_DIR + '/data/all_pred.csv') as f:
            reader = csv.reader(f, delimiter=',')

            count = 0

            header = None
            for row in reader:
                if header is None:
                    header = row
                    continue

                count += 1

                student_sample = MechTaskStudentSample()

                student_sample.index_in_dataframe = count

                float_row = [float(x) for x in row]

                # male: Whether the student is male (1/0)
                student_sample.male = False
                if float_row[header.index('male')] == 1:
                    student_sample.male = True

                # preschool: Whether the student attended preschool (1/0)
                student_sample.preschool = False
                if float_row[header.index('preschool')] == 1:
                    student_sample.preschool = True

                # expectBachelors: Whether the student expects to obtain a bachelor's
                # degree (1/0)
                student_sample.expectBachelors = False
                if float_row[header.index('expectBachelors')] == 1:
                    student_sample.expectBachelors = True

                # motherHS: Whether the student's mother completed high school (1/0)
                student_sample.motherHS = False
                if float_row[header.index('motherHS')] == 1:
                    student_sample.motherHS = True

                # motherBachelors: Whether the student's mother obtained a bachelor's
                # degree (1/0)
                student_sample.motherBachelors = False
                if float_row[header.index('motherBachelors')] == 1:
                    student_sample.motherBachelors = True

                # motherWork: Whether the student's mother has part-time or full-time work
                # (1/0)
                student_sample.motherWork = False
                if float_row[header.index('motherWork')] == 1:
                    student_sample.motherWork = True

                # fatherHS: Whether the student's father completed high school (1/0)
                student_sample.fatherHS = False
                if float_row[header.index('fatherHS')] == 1:
                    student_sample.fatherHS = True

                # fatherBachelors: Whether the student's father obtained a bachelor's
                # degree (1/0)
                student_sample.fatherBachelors = False
                if float_row[header.index('fatherBachelors')] == 1:
                    student_sample.fatherBachelors = True

                # fatherWork: Whether the student's father has part-time or full-time work
                # (1/0)
                student_sample.fatherWork = False
                if float_row[header.index('fatherWork')] == 1:
                    student_sample.fatherWork = True

                # selfBornUS: Whether the student was born in the United States of America
                # (1/0)
                student_sample.selfBornUS = False
                if float_row[header.index('selfBornUS')] == 1:
                    student_sample.selfBornUS = True

                # motherBornUS: Whether the student's mother was born in the United States
                # of America (1/0)
                student_sample.motherBornUS = False
                if float_row[header.index('motherBornUS')] == 1:
                    student_sample.motherBornUS = True

                # fatherBornUS: Whether the student's father was born in the United States
                # of America (1/0)
                student_sample.fatherBornUS = False
                if float_row[header.index('fatherBornUS')] == 1:
                    student_sample.fatherBornUS = True

                # englishAtHome: Whether the student speaks English at home (1/0)
                student_sample.englishAtHome = False
                if float_row[header.index('englishAtHome')] == 1:
                    student_sample.englishAtHome = True

                # computerForSchoolwork: Whether the student has access to a computer for
                # schoolwork (1/0)
                student_sample.computerForSchoolwork = False
                if float_row[header.index('computerForSchoolwork')] == 1:
                    student_sample.computerForSchoolwork = True

                # read30MinsADay: Whether the student reads for pleasure for 30 minutes/day
                # (1/0)
                student_sample.read30MinsADay = False
                if float_row[header.index('read30MinsADay')] == 1:
                    student_sample.read30MinsADay = True

                # minutesPerWeekEnglish: The number of minutes per week the student spend
                # in English class
                student_sample.minutesPerWeekEnglish = float_row[header.index(
                    'minutesPerWeekEnglish')]

                # studentsInEnglish: The number of students in this student's English class
                # at school
                student_sample.studentsInEnglish = int(
                    float_row[header.index('studentsInEnglish')])

                # schoolHasLibrary: Whether this student's school has a library (1/0)
                student_sample.schoolHasLibrary = False
                if float_row[header.index('schoolHasLibrary')] == 1:
                    student_sample.schoolHasLibrary = True

                # publicSchool: Whether this student attends a public school (1/0)
                student_sample.publicSchool = False
                if float_row[header.index('publicSchool')] == 1:
                    student_sample.publicSchool = True

                # urban: Whether this student's school is in an urban area (1/0)
                student_sample.urban = False
                if float_row[header.index('urban')] == 1:
                    student_sample.urban = True

                # schoolSize: The number of students in this student's school
                student_sample.schoolSize = int(
                    float_row[header.index('schoolSize')])

                # Race or ethnicity
                # The column names are:
                #   cat_raceeth_Asian
                #   cat_raceeth_Black
                #   cat_raceeth_Hispanic
                #   cat_raceeth_More than one race
                #   cat_raceeth_Native Hawaiian/Other Pacific Islander
                #   cat_raceeth_White

                if float_row[header.index('cat_raceeth_Asian')] == 1:
                    student_sample.raceeth = 'Asian'
                elif float_row[header.index('cat_raceeth_Black')] == 1:
                    student_sample.raceeth = 'Black'
                elif float_row[header.index('cat_raceeth_Hispanic')] == 1:
                    student_sample.raceeth = 'Hispanic'
                elif float_row[header.index('cat_raceeth_More than one race')] == 1:
                    student_sample.raceeth = 'More than one race'
                elif float_row[header.index('cat_raceeth_Native Hawaiian/Other Pacific Islander')] == 1:
                    student_sample.raceeth = 'Native Hawaiian/Other Pacific Islander'
                elif float_row[header.index('cat_raceeth_White')] == 1:
                    student_sample.raceeth = 'White'
                else:
                    student_sample.raceeth = 'Unknown'

                # Record the model scores
                student_sample.real_score = float_row[header.index(
                    'y_true')] * 100
                student_sample.linear_regression_prediction = float_row[header.index(
                    'LinearRegressioy_pred')] * 100
                student_sample.ridge_prediction = float_row[header.index(
                    'Ridge(alpha=0.0y_pred')] * 100
                student_sample.lasso_prediction = float_row[header.index(
                    'Lasso(alpha=1e-y_pred')] * 100
                student_sample.decision_tree_prediction = float_row[header.index(
                    'DecisionTreeRegy_pred')] * 100
                student_sample.random_forest_prediction = float_row[header.index(
                    'RandomForestRegy_pred')] * 100
                student_sample.kneighbors_prediction = float_row[header.index(
                    'KNeighborsRegrey_pred')] * 100
                student_sample.svm_reg_prediction = float_row[header.index(
                    'SVR(C=0.05)y_pred')] * 100

                student_sample.save()

    def create_user_groups(self):
        user_groups = OrderedDict({
            'cant-change-outcome': {
                'name': 'Cannot change outcome',
                'attention_check': "If you choose to use the model, you will not be able to change the model's predictions.  You will make predictions no matter which option you choose.",
            },
            'use-freely': {
                'name': 'Use freely',
                'attention_check': "use the model's predicted percentiles as much as you would like to. For each prediction, you will see the model's prediction and you can modify it as much as you like to form your official prediction.",
            },
            'adjust-by-10-original': {
                'name': 'Adjust by 10 percentiles',
                'attention_check': "If you choose to use the statistical model's predictions, you will be able to adjust the model's prediction for each student by up to 10 percentiles to form your official prediction.",
            },
            'adjust-by-10-proposed': {
                'name': 'Adjust by 10 percentiles - new bonus scheme',
                'attention_check': "If you choose to use the statistical model's predictions, you will be able to adjust the model's prediction for each student by up to 10 percentiles to form your official prediction.",
            },
            'cant-change-design': {
                'name': 'Cannot change design',
                'attention_check': 'If you choose to use the statistical model, you can adjust the predictions freely to form your official predictions. If you choose to use your own estimation, you will form your own official predictions based on the data.',
            },
            'change-input': {
                'name': 'Change input',
                'attention_check': 'If you choose to use the statistical model, you can adjust the predictions freely to form your predictions. If you choose to use your own estimation, you will receive the same information you picked and form your own predictions.',
                'extra_attention_check': 'you have a say in specifying the input into the model'
            },
            'change-algorithm': {
                'name': 'Change algorithm',
                'attention_check': 'If you choose to use the statistical model, you can adjust the predictions freely to form your own predictions. If you choose to use your own estimation, you will form your own predictions based on the data.',
                'extra_attention_check': 'you have a say in specifying the algorithm the model uses'
            },
            'change-input-placebo': {
                'name': 'Change input - placebo',
                'attention_check': 'If you choose to use the statistical model, you can adjust the predictions freely to form your official predictions. If you choose to use your own estimation, you will receive the same information you picked and form your own official predictions.',
                'extra_attention_check': 'you have a say in specifying the input into the model'
            },
            'change-algorithm-placebo': {
                'name': 'Change algorithm - placebo',
                'attention_check': 'If you choose to use the statistical model, you can adjust the predictions freely to form your own predictions. If you choose to use your own estimation, you will form your own predictions based on the data.',
                'extra_attention_check': 'you have a say in specifying the algorithm the model uses'
            },
            'change-input-cant-change-outcome': {
                'name': 'Change input - cannot change outcome',
                'attention_check': "If you choose to use the model, you will not be able to change the model's predictions.  You will make predictions no matter which option you choose.",
                'extra_attention_check': 'you have a say in specifying the input into the model'
            },
            'change-algorithm-cant-change-outcome': {
                'name': 'Change algorithm - cannot change outcome',
                'attention_check': "If you choose to use the model, you will not be able to change the model's predictions.  You will make predictions no matter which option you choose.",
                'extra_attention_check': 'you have a say in specifying the algorithm the model uses.'
            }
        })

        deception_groups = ['change-input-placebo', 'change-algorithm-placebo']

        allow_only_10_percentile_change = ['adjust-by-10-original',
                                           'adjust-by-10-proposed']

        change_algo_groups = ['change-algorithm', 'change-algorithm-placebo', 'change-algorithm-cant-change-outcome']

        change_attributes_groups = ['change-input', 'change-input-placebo', 'change-input-cant-change-outcome']

        new_bonus_scheme_groups = ['adjust-by-10-proposed']

        should_use_model_estimates_only_for_bonus = ['cant-change-outcome', \
        'change-input-cant-change-outcome', 'change-algorithm-cant-change-outcome']

        use_freely = ['use-freely']

        for slug in user_groups:
            ug = MechTaskUserGroup()
            ug.slug = slug
            ug.name = user_groups[slug]['name']
            ug.attention_check_statement = user_groups[slug]['attention_check']

            ug.has_deception = False
            if slug in deception_groups:
                ug.has_deception = True

            ug.only_10_percentile_change = False
            if slug in allow_only_10_percentile_change:
                ug.only_10_percentile_change = True

            ug.can_change_algorithm = False
            if slug in change_algo_groups:
                ug.can_change_algorithm = True
                ug.algo_attr_attention_check_statement = user_groups[slug]['extra_attention_check']

            ug.can_change_attributes = False
            if slug in change_attributes_groups:
                ug.can_change_attributes = True
                ug.algo_attr_attention_check_statement = user_groups[slug]['extra_attention_check']

            ug.uses_proposed_payment_scheme = False
            if slug in new_bonus_scheme_groups:
                ug.uses_proposed_payment_scheme = True

            ug.use_model_estimates_only = False
            if slug in should_use_model_estimates_only_for_bonus:
                ug.use_model_estimates_only = True

            ug.use_freely = False
            if slug in use_freely:
                ug.use_freely = True

            ug.save()

    def create_algorithms(self):
        algorithms = OrderedDict({
            'linear-regression': {
                'name': 'Linear regression',
                'avg_error': 19.7
            },
            # 'ridge-regression': {
            #     'name': 'Ridge regression',
            #     'avg_error': 19.7
            # },
            'lasso-regression': {
                'name':  'Lasso regression',
                'avg_error': 19.7
            },
            'decision-tree-regression': {
                'name': 'Decision tree regression',
                'avg_error': 20.80
            },
            'random-forest-regression':  {
                'name': 'Random forest regression',
                'avg_error': 20.20
            },
            'kneighbors-regression': {
                'name': 'K neighbors regression',
                'avg_error': 21.00
            },
            # 'svm-regression':  {
            #     'name': 'SVM regression',
            #     'avg_error': 19.90
            # },
        })

        for slug in algorithms:
            algorithm = MechTaskAlgorithm()
            algorithm.slug = slug
            algorithm.name = algorithms[slug]['name']
            algorithm.average_error = algorithms[slug]['avg_error']
            algorithm.save()

    def get(self, request):
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('home_page'))

        self.create_user_groups()
        self.create_algorithms()
        self.import_student_samples()

        return HttpResponse('Everything is set up!')
