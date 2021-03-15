import csv
from pathlib import Path

from django.shortcuts import (HttpResponse, HttpResponseRedirect, render,
                              reverse)
from django.views import View

from webapp.models import MechTaskStudentSample


class SetupMechTaskView(View):
    def get(self, request):
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('home_page'))

        BASE_DIR = str(Path(__file__).resolve().parent)

        with open(BASE_DIR + '/data/all_pred.csv') as f:
            reader = csv.reader(f, delimiter=',')

            count = 0

            header = None
            for row in reader:
                if header is None:
                    header = row
                    print(header)
                    continue

                count += 1

                student_sample = MechTaskStudentSample()

                student_sample.index_in_dataframe = count

                float_row = [float(x) for x in row]

                # male: Whether the student is male (1/0)
                if float_row[header.index('male')] == 1:
                    student_sample.male = True
                else:
                    student_sample.male = False

                # preschool: Whether the student attended preschool (1/0)
                if float_row[header.index('preschool')] == 1:
                    student_sample.pre_school = True
                else:
                    student_sample.pre_school = False

                # expectBachelors: Whether the student expects to obtain a bachelor's
                # degree (1/0)
                if float_row[header.index('expectBachelors')] == 1:
                    student_sample.expect_bachelors = True
                else:
                    student_sample.expect_bachelors = False

                # motherHS: Whether the student's mother completed high school (1/0)
                if float_row[header.index('motherHS')] == 1:
                    student_sample.mother_hs = True
                else:
                    student_sample.mother_hs = False

                # motherBachelors: Whether the student's mother obtained a bachelor's
                # degree (1/0)
                if float_row[header.index('motherBachelors')] == 1:
                    student_sample.mother_bachelors = True
                else:
                    student_sample.mother_bachelors = False

                # motherWork: Whether the student's mother has part-time or full-time work
                # (1/0)
                if float_row[header.index('motherWork')] == 1:
                    student_sample.mother_work = True
                else:
                    student_sample.mother_work = False

                # fatherHS: Whether the student's father completed high school (1/0)
                if float_row[header.index('fatherHS')] == 1:
                    student_sample.father_hs = True
                else:
                    student_sample.father_hs = False

                # fatherBachelors: Whether the student's father obtained a bachelor's
                # degree (1/0)
                if float_row[header.index('fatherBachelors')] == 1:
                    student_sample.father_bachelors = True
                else:
                    student_sample.father_bachelors = False

                # fatherWork: Whether the student's father has part-time or full-time work
                # (1/0)
                if float_row[header.index('fatherWork')] == 1:
                    student_sample.father_work = True
                else:
                    student_sample.father_work = False

                # selfBornUS: Whether the student was born in the United States of America
                # (1/0)
                if float_row[header.index('selfBornUS')] == 1:
                    student_sample.self_born_us = True
                else:
                    student_sample.self_born_us = False

                # motherBornUS: Whether the student's mother was born in the United States
                # of America (1/0)
                if float_row[header.index('motherBornUS')] == 1:
                    student_sample.mother_born_us = True
                else:
                    student_sample.mother_born_us = False

                # fatherBornUS: Whether the student's father was born in the United States
                # of America (1/0)
                if float_row[header.index('fatherBornUS')] == 1:
                    student_sample.father_born_us = True
                else:
                    student_sample.father_born_us = False

                # englishAtHome: Whether the student speaks English at home (1/0)
                if float_row[header.index('englishAtHome')] == 1:
                    student_sample.english_at_home = True
                else:
                    student_sample.english_at_home = False

                # computerForSchoolwork: Whether the student has access to a computer for
                # schoolwork (1/0)
                if float_row[header.index('computerForSchoolwork')] == 1:
                    student_sample.computer_for_schoolwork = True
                else:
                    student_sample.computer_for_schoolwork = False

                # read30MinsADay: Whether the student reads for pleasure for 30 minutes/day
                # (1/0)
                if float_row[header.index('read30MinsADay')] == 1:
                    student_sample.read_30_mins_a_day = True
                else:
                    student_sample.read_30_mins_a_day = False

                # minutesPerWeekEnglish: The number of minutes per week the student spend
                # in English class
                student_sample.minutes_per_week_english = float_row[header.index(
                    'minutesPerWeekEnglish')]

                # studentsInEnglish: The number of students in this student's English class
                # at school
                student_sample.students_in_english = int(
                    float_row[header.index('studentsInEnglish')])

                # schoolHasLibrary: Whether this student's school has a library (1/0)
                if float_row[header.index('schoolHasLibrary')] == 1:
                    student_sample.school_has_library = True
                else:
                    student_sample.school_has_library = False

                # publicSchool: Whether this student attends a public school (1/0)
                if float_row[header.index('publicSchool')] == 1:
                    student_sample.public_school = True
                else:
                    student_sample.public_school = False

                # urban: Whether this student's school is in an urban area (1/0)
                if float_row[header.index('urban')] == 1:
                    student_sample.urban = True
                else:
                    student_sample.urban = False

                # schoolSize: The number of students in this student's school
                student_sample.school_size = int(
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
                    student_sample.race_eth = 'Asian'
                elif float_row[header.index('cat_raceeth_Black')] == 1:
                    student_sample.race_eth = 'Black'
                elif float_row[header.index('cat_raceeth_Hispanic')] == 1:
                    student_sample.race_eth = 'Hispanic'
                elif float_row[header.index('cat_raceeth_More than one race')] == 1:
                    student_sample.race_eth = 'More than one race'
                elif float_row[header.index('cat_raceeth_Native Hawaiian/Other Pacific Islander')] == 1:
                    student_sample.race_eth = 'Native Hawaiian/Other Pacific Islander'
                elif float_row[header.index('cat_raceeth_White')] == 1:
                    student_sample.race_eth = 'White'
                else:
                    student_sample.race_eth = 'Unknown'

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

        return HttpResponse('Hello, world!')
