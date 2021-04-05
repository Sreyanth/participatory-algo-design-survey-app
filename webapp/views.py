import random
import uuid
from collections import OrderedDict

import numpy as np
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import (HttpResponse, HttpResponseRedirect, render,
                              reverse)
from django.views import View

from .models import (MechTaskAlgorithm, MechTaskStudentSample,
                     MechTaskSurveyEstimate, MechTaskSurveyResponse,
                     MechTaskUserGroup)

STUDENT_ATTRIBUTES = OrderedDict()
STUDENT_ATTRIBUTES['Student Characteristics'] = [
    {
        'text_to_show': 'Gender',
        'attr_id': 'male',
        'description': 'The gender of the student',
    },
    {
        'text_to_show': 'Race/Ethnicity',
        'attr_id': 'raceeth',
        'description': 'The race / ethnicity of the student',
    },
    {
        'text_to_show': 'Attended Pre-school',
        'attr_id': 'preschool',
        'description': 'Whether the student attended preschool',
    },
    {
        'text_to_show': 'Expects Bachelor',
        'attr_id': 'expectBachelors',
        'description': "Whether the student expects to obtain a bachelor's degree",
    },
]

STUDENT_ATTRIBUTES['Study Experience Characteristics'] = [
    {
        'text_to_show': 'Has Computer for School Work',
        'attr_id': 'computerForSchoolwork',
        'description': 'Whether the student has access to a computer for schoolwork',
    },
    {
        'text_to_show': 'Read 30min A Day',
        'attr_id': 'read30MinsADay',
        'description': 'Whether the student reads for pleasure for 30 minutes/day',
    },
    {
        'text_to_show': 'Minutes Per Week Spent in English',
        'attr_id': 'minutesPerWeekEnglish',
        'description': 'The number of minutes per week the student spend in English class',
    },
]

STUDENT_ATTRIBUTES['School Characteristics'] = [
    {
        'text_to_show': 'Number of Student in English',
        'attr_id': 'studentsInEnglish',
        'description': "The number of students in this student's English class at school",
    },
    {
        'text_to_show': 'School Has Library',
        'attr_id': 'schoolHasLibrary',
        'description': "Whether this student's school has a library",
    },
    {
        'text_to_show': 'Public School',
        'attr_id': 'publicSchool',
        'description': 'Whether this student attends a public school',
    },
    {
        'text_to_show': 'Urban',
        'attr_id': 'urban',
        'description': "Whether this student's school is in an urban area",
    },
    {
        'text_to_show': 'School Size',
        'attr_id': 'schoolSize',
        'description': "The number of students in this student's school",
    },
]

STUDENT_ATTRIBUTES['Parental Characteristics'] = [
    {
        'text_to_show': 'Mother Completed High School',
        'attr_id': 'motherHS',
        'description': "Whether the student's mother completed high school",
    },
    {
        'text_to_show': "Mother Has Bachelor's Degree",
        'attr_id': 'motherBachelors',
        'description': "Whether the student's mother obtained a bachelor's degree",
    },
    {
        'text_to_show': 'Mother Works',
        'attr_id': 'motherWork',
        'description': "Whether the student's mother has part-time or full-time work",
    },
    {
        'text_to_show': 'Father Completed High School',
        'attr_id': 'fatherHS',
        'description': "Whether the student's father completed high school",
    },
    {
        'text_to_show': "Father Has Bachelor's Degree",
        'attr_id': 'fatherBachelors',
        'description': "Whether the student's father obtained a bachelor's degree",
    },
    {
        'text_to_show': 'Father Works',
        'attr_id': 'fatherWork',
        'description': "Whether the student's father has part-time or full-time work",
    },
]

STUDENT_ATTRIBUTES['Family Characteristics'] = [
    {
        'text_to_show': 'Student born in the US',
        'attr_id': 'selfBornUS',
        'description': 'Whether the student was born in the United States of America',
    },
    {
        'text_to_show': "Mother born in the US",
        'attr_id': 'motherBornUS',
        'description': "Whether the student's mother was born in the United States of America",
    },
    {
        'text_to_show': 'Father born in the US',
        'attr_id': 'fatherBornUS',
        'description': "Whether the student's father was born in the United States of America",
    },
    {
        'text_to_show': 'Speak English at Home',
        'attr_id': 'englishAtHome',
        'description': 'Whether the student speaks English at home',
    },
]


def user_fails_access_check(request):
    if not request.user.is_authenticated:
        return True

    try:
        request.user.mech_task_survey_response
        return False
    except ObjectDoesNotExist:
        return True


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class StartSurveyView(View):
    def create_and_get_new_user(self):
        """
        Create a new user with a random username.
        """

        new_user = User()
        new_user.username = uuid.uuid4()
        new_user.save()

        return new_user

    def create_survey_response(self, request):
        """
        Create a new response template for the user.

        We will use this response to keep track of where the user is in the survey.
        """

        survey_response = MechTaskSurveyResponse()
        survey_response.user = request.user

        # Randomly assign a survey group
        # Right now, we fetch all groups all the time. We can optimize this.
        # TODO: optimize this workflow.

        survey_response.user_group = random.choice(
            MechTaskUserGroup.objects.all())

        survey_response.save()

    def get(self, request):
        """
        GET /start

        If the user is visiting this URL for the first time, a new user is created
        and a random survey group is assigned.

        The user is then taken to the consent page.
        """

        if not request.user.is_authenticated:
            # Since the user is new here, we will create a random user for tracking
            # And create a authenticated session for the random user
            user = self.create_and_get_new_user()
            login(request, user)

        try:
            request.user.mech_task_survey_response
        except ObjectDoesNotExist:
            # Since the user is new here, we will create a new survey response now
            self.create_survey_response(request)

        return HttpResponseRedirect(reverse('mech_task_consent'))


class ConsentView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if survey_response.user_consented_to_survey:
            return HttpResponseRedirect(reverse('mech_task_instructions'))

        page_params = {
            'user': request.user,
            'user_group': survey_response.user_group.slug
        }

        return render(request, 'consent.html', page_params)

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if survey_response.user_consented_to_survey:
            # This most likely won't be possible, but handling just in case
            return HttpResponseRedirect(reverse('mech_task_instructions'))

        submitted_form = request.POST

        age_check = submitted_form.get('age_check')
        consent_check = submitted_form.get('consent_check')
        read_information_check = submitted_form.get(
            'read_information_check')
        mturk_id_1 = submitted_form.get('mturk_id_1').strip()
        mturk_id_2 = submitted_form.get('mturk_id_2').strip()

        error_message = None

        if age_check != 'true':
            error_message = 'You can take this survey only if you are 18 or older'
        elif read_information_check != 'true':
            error_message = 'You need to read and understand the information above'
        elif consent_check != 'true':
            error_message = 'You need to consent to the survey policies to continue'
        elif len(mturk_id_1) == 0:
            error_message = 'You need to input your MTurk ID to proceed'
        elif len(mturk_id_2) == 0:
            error_message = 'You need to reconfirm your MTurk ID to proceed'
        elif mturk_id_1 != mturk_id_2:
            error_message = "The MTurk IDs you provided don't match. Try again"

        if error_message:
            page_params = {
                'error_message': error_message,
                'age_check': age_check,
                'read_information_check': read_information_check,
                'consent_check': consent_check,
                'mturk_id_1': mturk_id_1,
                'mturk_id_2': mturk_id_2
            }
            return render(request, 'consent.html', page_params)

        # No errors! Let's record the inputs and move on!
        survey_response.user_is_18_or_older = True
        survey_response.user_read_and_understood_info = True
        survey_response.user_wants_to_participate = True
        survey_response.user_consented_to_survey = True
        survey_response.mturk_id_attempt_1 = mturk_id_1
        survey_response.current_stage = 'instructions'

        survey_response.save()

        return HttpResponseRedirect(reverse('mech_task_instructions'))


class InstructionsView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        return render(request, 'instructions.html')

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        survey_response.read_first_instruction = True
        survey_response.read_percentile_description = True
        survey_response.save()

        return HttpResponseRedirect(reverse('mech_task_understand_datapoints'))


class UnderstandDataView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        return render(request, 'understand-data.html')

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        survey_response.read_sample_data_points = True
        survey_response.save()

        return HttpResponseRedirect(reverse('mech_task_choose_algorithm'))
        # return HttpResponseRedirect(reverse('mech_task_understand_model'))


class ChooseAlgorithmView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if not survey_response.user_group.can_change_algorithm:
            survey_response.algorithm = MechTaskAlgorithm.objects.get(id=1)
            survey_response.save()

        if survey_response.algorithm is not None:
            # User already selected an algorithm
            return HttpResponseRedirect(reverse('mech_task_choose_attributes'))

        algorithms = MechTaskAlgorithm.objects.all()
        return render(request, 'choose-algorithm.html', {'algorithms': algorithms})

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        user_selected_algo = request.POST.get('algorithm').strip()

        try:
            algorithm = MechTaskAlgorithm.objects.get(
                slug=user_selected_algo)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('mech_task_choose_attributes'))

        survey_response = request.user.mech_task_survey_response
        survey_response.user_selected_algorithm = algorithm

        if survey_response.user_group.has_deception:
            # Now, select a random algorithm
            deception_algo_choices = [
                'linear-regression',
                'ridge-regression',
                'lasso-regression',
                'decision-tree-regression',
                'random-forest-regression',
                'kneighbors-regression',
                'svm-regression',
            ]

            deception_algo_choices.remove(user_selected_algo)

            random_algo = random.choice(deception_algo_choices)
            algorithm = MechTaskAlgorithm.objects.get(
                slug=random_algo)

        survey_response.algorithm = algorithm
        survey_response.save()

        return HttpResponseRedirect(reverse('mech_task_choose_attributes'))


class ChooseAttributesView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if not survey_response.user_group.can_change_attributes:
            survey_response.selected_attributes = 'all'
            survey_response.save()

        if survey_response.selected_attributes is not None:
            # User already selected the attributes
            return HttpResponseRedirect(reverse('mech_task_understand_model'))

        return render(request, 'choose-attributes.html', {'attributes': STUDENT_ATTRIBUTES})

    def post(self, request):
        pass


class UnderstandModelView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if survey_response.model:
            page_params = {'avg_err': survey_response.model.average_error}
        else:
            page_params = {'avg_err': survey_response.algorithm.average_error}

        return render(request, 'understand-model.html', page_params)

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        survey_response.read_model_description = True
        survey_response.read_that_model_is_off = True
        survey_response.save()

        return HttpResponseRedirect(reverse('mech_task_attention_check'))


class AttentionCheckView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if survey_response.passed_first_attention_check:
            return HttpResponseRedirect(reverse('mech_task_choose_bonus'))

        page_params = {
            'attention_text': survey_response.user_group.attention_check_statement,
            'user_group': survey_response.user_group.slug,
        }

        return render(request, 'attention-check.html', page_params)

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response
        attention_statement = survey_response.user_group.attention_check_statement.strip()

        submitted_form = request.POST
        submitted_attention_statement = submitted_form.get(
            'important-check').strip()

        if attention_statement.lower() == submitted_attention_statement.lower():
            # Attention check passed
            survey_response.passed_first_attention_check = True
            survey_response.save()

            return HttpResponseRedirect(reverse('mech_task_choose_bonus'))

        error_message = 'Please enter the underlined text.'

        page_params = {'attention_text': survey_response.user_group.attention_check_statement,
                       'error_message': error_message, 'submitted_attention_statement': submitted_attention_statement, }

        return render(request, 'attention-check.html', page_params)


class ChooseBonusView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if survey_response.chose_bonus_baseline:
            return HttpResponseRedirect(reverse('mech_task_survey_question'))

        return render(request, 'choose-bonus.html')

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        submitted_form = request.POST

        attention_statement = '''
        During the official round, you will receive additional bonus money based on the accuracy of the official estimates. You can earn $1 to $5 depending on how close the official estimates are to the actual ranks.
        '''.strip().replace('\n', '').replace('\t', '')

        submitted_attention_statement = submitted_form.get(
            'important-check').strip().replace('\n', '')

        error_message = None

        if attention_statement.lower() != submitted_attention_statement.lower():
            error_message = 'Please enter the underlined text.'

        bonus_choice = submitted_form.get('bonus_preference').strip()
        if bonus_choice not in ['model', 'self']:
            error_message = 'Please select your bonus preference.'

        if error_message:
            page_params = {
                'error_message': error_message, 'submitted_attention_statement': submitted_attention_statement, }

            return render(request, 'choose-bonus.html', page_params)

        survey_response.passed_second_attention_check = True
        survey_response.chose_bonus_baseline = True
        if bonus_choice == 'model':
            survey_response.use_model_estimates_for_bonus_calc = True
        else:
            survey_response.use_model_estimates_for_bonus_calc = False

        survey_response.save()
        return HttpResponseRedirect(reverse('mech_task_survey_question'))


class SurveyView(View):
    def assign_questions(self, survey_response):
        # Should we assign custom model questions or choose from the original
        # question bank?

        selected_attributes = survey_response.selected_attributes
        selected_algo = survey_response.algorithm.slug

        if selected_attributes and selected_attributes == 'all':
            # Pick questions from the question bank
            # TODO: Optimize this flow. Right now it selects all objects?
            # One way to do is a randomize on range(723) and select only those
            # objects

            if selected_algo.startswith('linear'):
                model_estimate_field = 'linear_regression_prediction'
            elif selected_algo.startswith('ridge'):
                model_estimate_field = 'ridge_prediction'
            elif selected_algo.startswith('lasso'):
                model_estimate_field = 'lasso_prediction'
            elif selected_algo.startswith('decision'):
                model_estimate_field = 'decision_tree_prediction'
            elif selected_algo.startswith('random'):
                model_estimate_field = 'random_forest_prediction'
            elif selected_algo.startswith('svm'):
                model_estimate_field = 'svm_reg_prediction'

            selected_student_ids = []

            while len(selected_student_ids) < 20:
                random_id = random.randint(1, 724)
                # Select only those students whose relevant model score is gt 0
                kwargs = {
                    model_estimate_field + '__gt': 0,
                    # 'id__exact': random_id,
                    'index_in_dataframe__exact': random_id,
                }

                student = MechTaskStudentSample.objects.filter(
                    **kwargs).first()

                if not student:
                    continue

                selected_student_ids.append(random_id)

                estimate = MechTaskSurveyEstimate()
                estimate.survey_response = survey_response
                estimate.sample = student
                estimate.model_estimate = getattr(
                    student, model_estimate_field)
                estimate.real_score = student.real_score
                estimate.save()

        else:
            # The questions should've been already assigned to the user when we created the model
            pass

    def calculate_bonus(self, survey_response):
        bonus_scheme = OrderedDict({
            5: 5,
            10: 4,
            15: 3,
            20: 2,
            25: 1,
        })

        bonus_scheme_v2 = OrderedDict({
            14: 5,
            17: 4,
            20: 3,
            23: 2,
            26: 1,
        })

        estimates = survey_response.survey_estimates.all()
        use_model_for_bonus = survey_response.use_model_estimates_for_bonus_calc

        user_estimates = []
        y_trues = []

        for estimate in estimates:
            y_trues.append(estimate.real_score)
            if use_model_for_bonus:
                user_estimates.append(estimate.model_estimate)
            else:
                user_estimates.append(estimate.user_estimate)

        devs = [a_i - b_i for a_i, b_i in zip(user_estimates, y_trues)]
        devs = [np.abs(i) for i in devs]
        avg_devs = np.mean(devs)

        bonus_calc_to_use = bonus_scheme

        if survey_response.user_group.uses_proposed_payment_scheme:
            bonus_calc_to_use = bonus_scheme_v2

        bonus = 0

        for limit in bonus_calc_to_use:
            if avg_devs <= limit:
                bonus = bonus_calc_to_use[limit]
                break

        survey_response.bonus = bonus
        survey_response.average_deviation = avg_devs
        survey_response.save()

    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if survey_response.survey_estimates.count() == 0:
            self.assign_questions(survey_response)

        try:
            # Get one question from the allotted questions
            question = survey_response.survey_estimates.filter(completed=False)[
                0]
        except IndexError:
            # There are no more questions
            self.calculate_bonus(survey_response)
            return HttpResponseRedirect(reverse('mech_task_follow_up_questions'))

        page_params = {
            'question': question,
            'sample': question.sample,
            'use_model_estimates_for_bonus_calc': survey_response.use_model_estimates_for_bonus_calc,
        }

        return render(request, 'survey.html', page_params)

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home_page'))

        try:
            survey_response = request.user.mech_task_survey_response
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('home_page'))

        question_id = request.POST.get('question_id').strip()
        user_estimate = request.POST.get('user_estimate').strip()

        try:
            question = survey_response.survey_estimates.filter(
                completed=False, id=int(question_id))[0]
        except IndexError:
            return HttpResponseRedirect(reverse('mech_task_survey_question'))

        question.user_estimate = float(user_estimate)
        question.completed = True
        question.save()

        survey_response.number_of_estimates_done += 1
        survey_response.save()

        return HttpResponseRedirect(reverse('mech_task_survey_question'))


class FollowUpQuestionsView(View):
    def get_next_question(self, survey_response):
        follow_up_questions = OrderedDict({
            'model_estimate_average_error': {
                'question_text': 'On average, how many percentiles do you think the model’s estimates are away from students’ actual percentiles?',
                'sub_texts': ['An answer of zero would mean that you think the model perfectly estimates all of the percentiles. An answer of one would mean that you think the model’s estimates are off by 1 percentile, on average.', 'Your answer can range from 0-100.'],
                'type': 'number_input',
                'label': 'Enter your answer (0-100)',
            },
            'self_estimate_average_error': {
                'question_text': 'On average, how many percentiles do you think your estimates are away from students’ actual percentiles?',
                'sub_texts': ['An answer of zero would mean that you think you perfectly estimates all of the percentiles. An answer of one would mean that you think the model’s estimates are off by 1 percentile, on average.', 'Your answer can range from 0-100.'],
                'type': 'number_input',
                'label': 'Enter your answer (0-100)',
            },
            'model_estimate_confidence': {
                'question_text': 'How much confidence do you have in the statistical model’s estimates?',
                'type': 'likert',
                'scale': ['None', 'Little', 'Some', 'A Fair Amount', 'A Lot'],
            },
            'self_estimate_confidence': {
                'question_text': 'How much confidence do you have in your estimates?',
                'type': 'likert',
                'scale': ['None', 'Little', 'Some', 'A Fair Amount', 'A Lot'],
            },
            'why_chose_the_attributes': {
                'question_text': 'Why did you choose to use following factors to make your estimation?',
                'sub_texts': [survey_response.user_selected_attributes],
                'type': 'long_text',
            },
            'why_chose_the_algorithm': {
                'question_text': 'Why did you choose to use %s to make your estimation regardless you ended up using it or not?' % (survey_response.user_selected_algorithm.name),
                'type': 'long_text',
            },
            'why_chose_model_estimate': {
                'question_text': 'Why did you choose to have your bonus be determined by the statistical model’s estimates instead of your estimates?',
                'type': 'long_text',
            },
            'why_chose_self_estimate': {
                'question_text': 'Why did you choose to have your bonus be determined by your estimates instead of the statistical model’s estimates?',
                'type': 'long_text',
            },
            'representativeness': {
                'question_text': 'How well do you think the statistical model represent your assessment of the students’ performance?',
                'type': 'likert',
                'scale': ['Not representative at all', 'Slightly representative', 'Moderately representative', 'Very representative', 'Extremely representative'],
            },
            'transparency': {
                'question_text': 'How transparent would you rate the statistical model decision process? ',
                'type': 'likert',
                'scale': ['Not at all transparent', 'Slightly transparent', 'Moderately transparent', 'Very transparent', 'Extremely transparent'],
            },
            'fairness_tutoring_resources': {
                'question_text': 'Based on the scenarios you rated, would it be fair for the school to allocate tutoring resources to the students that the model predicts will have the lowest reading scores?',
                'type': 'long_text',
            },
            'fairness_scholarship': {
                'question_text': 'Based on the scenarios you rated, would it be fair for the school to recommend students with the highest predicted reading scores for a competitive scholarship in reading? ',
                'type': 'long_text',
            },
            'fairness_absent_students': {
                'question_text': 'Based on the scenarios you rated, would it be fair for the school to use the statistical model’s forecast to decide some part of the students’ final grade if the students were unable to attend exams?',
                'type': 'long_text',
            },
            # 'fairness_explanation': {
            #     'question_text': '',
            #     'type': '',
            #     'scale': [],
            # },
            'likeliness_to_use_model': {
                'question_text': 'How likely would you be to use the model’s estimates to complete this task in the future?',
                'type': 'likert',
                'scale': ['Very unlikely', 'unlikely', 'undecided', 'likely', 'very likely'],
            },
            'any_other_thoughts': {
                'question_text': 'Do you have any other thoughts and feelings about the statistical model? ',
                'type': 'long_text',
            },
        })

        self_estimates_only_questions = ['why_chose_self_estimate']

        model_estimates_only_questions = [
            'model_estimate_average_error',
            'model_estimate_confidence',
            'why_chose_model_estimate',
            'representativeness',
            'transparency',
            'fairness_tutoring_resources',
            'fairness_scholarship',
            'fairness_absent_students',
            'likeliness_to_use_model',
            'any_other_thoughts',
        ]

        for question in follow_up_questions:
            if survey_response.use_model_estimates_for_bonus_calc:
                # User selected the model for bonus calculations
                # So, skip questions that we should show only to people who
                # chose self estimates for bonus
                if question in self_estimates_only_questions:
                    continue
            else:
                # User selected to use the self estimates for bonus
                # So, skip questions that we should show only to people who
                # chose model estimates for bonus
                if question in model_estimates_only_questions:
                    continue

            if not survey_response.user_group.can_change_attributes:
                # User can't change attributes. So skip the related question
                if question in ['why_chose_the_attributes']:
                    continue

            if not survey_response.user_group.can_change_algorithm:
                # User can't select algorithm. So skip the related question
                if question in ['why_chose_the_algorithm']:
                    continue

            answer = getattr(survey_response, question)

            if answer:
                continue

            return question, follow_up_questions[question]

        return None, None

    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        question, question_details = self.get_next_question(survey_response)

        if not question:
            # All follow-up questions are done. Take the user to the exit_survey
            return HttpResponseRedirect(reverse('mech_task_exit_survey'))

        question_text = question_details['question_text']
        question_type = question_details['type']

        page_params = {
            'id': question,
            'text': question_text,
            'type': question_type,
        }

        if 'sub_texts' in question_details:
            page_params['subs'] = question_details['sub_texts']

        if 'scale' in question_details:
            page_params['scale'] = question_details['scale']

        if 'label' in question_details:
            page_params['label'] = question_details['label']

        return render(request, 'questions/' + question_type + '.html', page_params)

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        question_id = request.POST.get('question_id')

        answer = getattr(survey_response, question_id)

        if not answer:
            setattr(survey_response, question_id, request.POST.get('answer'))
            survey_response.save()

        return HttpResponseRedirect(reverse('mech_task_follow_up_questions'))


class ExitSurveyView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if survey_response.completed:
            return HttpResponseRedirect(reverse('mech_task_thanks'))

        exit_survey_questions = {
            'age': {
                'question_text': 'What is your age?',
                'options': range(18, 100)
            },
            'pronoun': {
                'question_text': 'What is your pronoun?',
                'options': ['He/his', 'she/her', 'they/their', 'other', 'I prefer not to answer']
            },
            'raceeth': {
                'question_text': 'How do you identify your race or ethnicity?',
                'options': ['White', 'Hispanic', 'Black or African American', 'Asian', 'American Indian or Alaska Native', 'Middle Eastern or North African', 'Native Hawaiian or other pacific islander', 'Multi', 'Other', 'I prefer not to answer']
            },
            'education': {
                'question_text': 'What is the highest level of education you have completed?',
                'options': ['Less than high school', 'high school/GED', 'some college', '2-year college degree', '4-year college degree', 'masters degree', 'professional degree(JD, MD)', 'Doctoral Degree', 'I prefer not to answer']
            },
        }

        return render(request, 'exit-survey.html', {'questions': exit_survey_questions})

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        survey_response.age_bracket = request.POST.get('age')
        survey_response.pronoun = request.POST.get('pronoun')
        survey_response.race_ethnicity = request.POST.get('raceeth')
        survey_response.highest_level_of_education = request.POST.get(
            'education')
        survey_response.mturk_id_attempt_2 = request.POST.get(
            'final_mturk_id').strip()

        if survey_response.mturk_id_attempt_1.strip() == survey_response.mturk_id_attempt_2.strip():
            survey_response.final_mturk_id = survey_response.mturk_id_attempt_1.strip()

        survey_response.completed = True
        survey_response.save()

        return HttpResponseRedirect(reverse('mech_task_thanks'))


class ThanksView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        page_params = {
            'bonus': survey_response.bonus,
            'show_debrief_form_link': survey_response.user_group.has_deception,
        }

        return render(request, 'thanks.html', page_params)
