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
                student_sample.real_score = float_row[header.index('y_true')]
                student_sample.linear_regression_prediction = float_row[header.index(
                    'LinearRegressioy_pred')]
                student_sample.ridge_prediction = float_row[header.index(
                    'Ridge(alpha=0.0y_pred')]
                student_sample.lasso_prediction = float_row[header.index(
                    'Lasso(alpha=1e-y_pred')]
                student_sample.decision_tree_prediction = float_row[header.index(
                    'DecisionTreeRegy_pred')]
                student_sample.random_forest_prediction = float_row[header.index(
                    'RandomForestRegy_pred')]
                student_sample.kneighbors_prediction = float_row[header.index(
                    'KNeighborsRegrey_pred')]
                student_sample.svm_reg_prediction = float_row[header.index(
                    'SVR(C=0.05)y_pred')]

                student_sample.save()

    def create_user_groups(self):
        user_groups = OrderedDict({
            'cannot-change-control': {
                'name': 'Cannot change - control group',
                'attention_check': 'What you want to type',
            },
            'use-freely': {
                'name': 'Use freely',
                'attention_check': 'What you want to type',
            },
            'change-outcome': {
                'name': 'Change outcome',
                'attention_check': 'What you want to type',
            },
            'change-outcome-proposed-payment': {
                'name': 'Change outcome - new bonus scheme',
                'attention_check': 'What you want to type',
            },
            'change-attributes': {
                'name': 'Change attributes',
                'attention_check': 'What you want to type',
            },
            'change-algorithm': {
                'name': 'Change algorithm',
                'attention_check': 'What you want to type',
            },
            'change-attributes-placebo': {
                'name': 'Change attributes - placebo',
                'attention_check': 'What you want to type',
            },
            'change-algorithm-placebo': {
                'name': 'Change algorithm - placebo',
                'attention_check': 'What you want to type',
            },
        })

        deception_groups = ['change-attributes-placebo',
                            'change-algorithm-placebo']

        change_algo_groups = ['change-algorithm', 'change-algorithm-placebo']

        change_attributes_groups = [
            'change-attributes', 'change-attributes-placebo']

        new_bonus_scheme_groups = ['change-outcome-proposed-payment']

        for slug in user_groups:
            ug = MechTaskUserGroup()
            ug.slug = slug
            ug.name = user_groups[slug]['name']
            ug.attention_check_statement = user_groups[slug]['attention_check']

            ug.has_deception = False
            if slug in deception_groups:
                ug.has_deception = True

            ug.can_change_algorithm = False
            if slug in change_algo_groups:
                ug.can_change_algorithm = True

            ug.can_change_attributes = False
            if slug in change_attributes_groups:
                ug.can_change_attributes = True

            ug.uses_proposed_payment_scheme = False
            if slug in new_bonus_scheme_groups:
                ug.uses_proposed_payment_scheme = True

            ug.save()

    def create_algorithms(self):
        algorithms = OrderedDict({
            'linear-regression': 'Linear regression',
            'ridge-regression': 'Ridge regression',
            'lasso-regression': 'Lasso regression',
            'decision-tree-regression': 'Decision tree regression',
            'random-forest-regression': 'Random forest regression',
            'kneighbors-regression': 'K neighbors regression',
            'svm-regression': 'SVM regression',
        })

        for slug in algorithms:
            algorithm = MechTaskAlgorithm()
            algorithm.slug = slug
            algorithm.name = algorithms[slug]
            algorithm.save()

    def get(self, request):
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('home_page'))

        self.create_user_groups()
        self.create_algorithms()
        self.import_student_samples()

        return HttpResponse('Everything is set up!')
