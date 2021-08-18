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
        'description': 'The gender of the student (female / male)',
    },
    {
        'text_to_show': 'Race / ethnicity',
        'attr_id': 'raceeth',
        'description': 'The race / ethnicity of the student',
    },
    {
        'text_to_show': 'Attended pre-school',
        'attr_id': 'preschool',
        'description': 'Whether the student attended preschool',
    },
    {
        'text_to_show': 'Expects a bachelor\'s degree',
        'attr_id': 'expectBachelors',
        'description': "Whether the student expects to obtain a bachelor's degree",
    },
]

STUDENT_ATTRIBUTES['Study Experience Characteristics'] = [
    {
        'text_to_show': 'Has a computer for school work',
        'attr_id': 'computerForSchoolwork',
        'description': 'Whether the student has access to a computer for schoolwork',
    },
    {
        'text_to_show': 'Reads 30 minutes a day',
        'attr_id': 'read30MinsADay',
        'description': 'Whether the student reads for pleasure for at least 30 minutes/day',
    },
    {
        'text_to_show': 'Minutes per week spent in English',
        'attr_id': 'minutesPerWeekEnglish',
        'description': 'The number of minutes per week the student spend in English class',
    },
]

STUDENT_ATTRIBUTES['School Characteristics'] = [
    {
        'text_to_show': 'Number of students in English class',
        'attr_id': 'studentsInEnglish',
        'description': "The number of students in this student's English class at school",
    },
    {
        'text_to_show': 'School has a library',
        'attr_id': 'schoolHasLibrary',
        'description': "Whether this student's school has a library",
    },
    {
        'text_to_show': 'Public school',
        'attr_id': 'publicSchool',
        'description': 'Whether this student attends a public school',
    },
    {
        'text_to_show': 'Urban',
        'attr_id': 'urban',
        'description': "Whether this student's school is in an urban area",
    },
    {
        'text_to_show': 'School size',
        'attr_id': 'schoolSize',
        'description': "The number of students in this student's school",
    },
]

STUDENT_ATTRIBUTES['Parental Characteristics'] = [
    {
        'text_to_show': 'Mother completed high school',
        'attr_id': 'motherHS',
        'description': "Whether the student's mother completed high school",
    },
    {
        'text_to_show': "Mother has a bachelor's degree",
        'attr_id': 'motherBachelors',
        'description': "Whether the student's mother obtained a bachelor's degree",
    },
    {
        'text_to_show': 'Mother works',
        'attr_id': 'motherWork',
        'description': "Whether the student's mother has a part-time or a full-time job",
    },
    {
        'text_to_show': 'Father completed high school',
        'attr_id': 'fatherHS',
        'description': "Whether the student's father completed high school",
    },
    {
        'text_to_show': "Father has a bachelor's degree",
        'attr_id': 'fatherBachelors',
        'description': "Whether the student's father obtained a bachelor's degree",
    },
    {
        'text_to_show': 'Father works',
        'attr_id': 'fatherWork',
        'description': "Whether the student's father has a part-time or a full-time work",
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
        'text_to_show': 'Speaks English at home',
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

        # survey_response.user_group = random.choice(
        #     MechTaskUserGroup.objects.all())

        survey_response.user_group = random.choice(
        MechTaskUserGroup.objects.get(id=1), MechTaskUserGroup.objects.get(id=2), MechTaskUserGroup.objects.get(id=3), \
        MechTaskUserGroup.objects.get(id=4))

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
            'user_group': survey_response.user_group
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
        only_once_check = submitted_form.get('only_once_check')
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
        elif only_once_check != 'true':
            error_message = 'You need to agree that you will take this survey only once to continue'
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
                'only_once_check': only_once_check,
                'mturk_id_1': mturk_id_1,
                'mturk_id_2': mturk_id_2
            }
            return render(request, 'consent.html', page_params)

        # No errors! Let's record the inputs and move on!
        survey_response.user_is_18_or_older = True
        survey_response.user_read_and_understood_info = True
        survey_response.user_wants_to_participate = True
        survey_response.user_consented_to_survey = True
        survey_response.user_agreed_to_take_only_once = True
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

        user_ans = request.POST.getlist('answers')
        user_understood_instruction = (user_ans == ['A', 'D'])

        survey_response = request.user.mech_task_survey_response
        survey_response.read_first_instruction = True
        survey_response.read_percentile_description = True
        survey_response.user_understood_first_instruction = user_understood_instruction
        survey_response.user_first_instruction_ans = user_ans
        survey_response.save()

        if survey_response.user_group.can_change_attributes:
            return HttpResponseRedirect(reverse('mech_task_pre_algo_attrs_check'))

        return HttpResponseRedirect(reverse('mech_task_understand_datapoints'))


class PreAlgoAttrsCheckView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if survey_response.passed_algo_attr_attention_check:
            return HttpResponseRedirect(reverse('mech_task_understand_datapoints'))

        page_params = {
            'attention_text': survey_response.user_group.algo_attr_attention_check_statement,
            'user_group': survey_response.user_group,
        }

        return render(request, 'pre-algo-attrs-check.html', page_params)

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response
        attention_statement = survey_response.user_group.algo_attr_attention_check_statement.strip()

        submitted_form = request.POST
        submitted_attention_statement = submitted_form.get(
            'important-check').strip()

        if attention_statement.lower().replace(' ', '') == submitted_attention_statement.lower().replace(' ', ''):
            # Attention check passed
            survey_response.passed_algo_attr_attention_check = True
            survey_response.save()

            return HttpResponseRedirect(reverse('mech_task_understand_datapoints'))

        error_message = 'Please enter the underlined text as is. You might be missing a word or some punctuation!'

        page_params = {
            'attention_text': survey_response.user_group.algo_attr_attention_check_statement,
            'error_message': error_message,
            'submitted_attention_statement': submitted_attention_statement,
            'user_group': survey_response.user_group,
        }

        return render(request, 'pre-algo-attrs-check.html', page_params)


class UnderstandDataView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        return render(request, 'understand-data.html', {'attributes': STUDENT_ATTRIBUTES, 'user_group': survey_response.user_group, })

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        survey_response.read_sample_data_points = True
        survey_response.save()

        if survey_response.user_group.can_change_algorithm:
            return HttpResponseRedirect(reverse('mech_task_pre_algo_check'))

        return HttpResponseRedirect(reverse('mech_task_choose_algorithm'))
        # return HttpResponseRedirect(reverse('mech_task_understand_model'))


class PreAlgoCheckView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if survey_response.passed_algo_attr_attention_check:
            return HttpResponseRedirect(reverse('mech_task_choose_algorithm'))

        page_params = {
            'attention_text': survey_response.user_group.algo_attr_attention_check_statement,
            'user_group': survey_response.user_group,
        }

        return render(request, 'pre-algo-check.html', page_params)

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response
        attention_statement = survey_response.user_group.algo_attr_attention_check_statement.strip()

        submitted_form = request.POST
        submitted_attention_statement = submitted_form.get(
            'important-check').strip()

        if attention_statement.lower().replace(' ', '') == submitted_attention_statement.lower().replace(' ', ''):
            # Attention check passed
            survey_response.passed_algo_attr_attention_check = True
            survey_response.save()

            return HttpResponseRedirect(reverse('mech_task_choose_algorithm'))

        error_message = 'Please enter the underlined text as is. You might be missing a word or some punctuation!'

        page_params = {
            'attention_text': survey_response.user_group.algo_attr_attention_check_statement,
            'error_message': error_message,
            'submitted_attention_statement': submitted_attention_statement,
            'user_group': survey_response.user_group,
        }

        return render(request, 'pre-algo-check.html', page_params)


class ChooseAlgorithmView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if not survey_response.user_group.can_change_algorithm:
            algorithm = MechTaskAlgorithm.objects.get(id=1)
            survey_response.algorithm = algorithm
            survey_response.user_selected_algorithm = algorithm
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
            selected_attributes = 'all'
            survey_response.selected_attributes = selected_attributes
            survey_response.user_selected_attributes = selected_attributes
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

        page_params['user_group'] = survey_response.user_group

        return render(request, 'understand-model.html', page_params)

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        survey_response.read_model_description = True
        survey_response.read_that_model_is_off = True
        survey_response.save()

        return HttpResponseRedirect(reverse('mech_task_understand_payment_structure'))


class UnderstandPaymentStructureView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        page_params = {
            'user_group': survey_response.user_group,
        }

        return render(request, 'understand-payment-structure.html', page_params)

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        submitted_form = request.POST

        attention_statement = '''
        You will receive additional bonus money based on the accuracy of the final predictions. You can earn $1 to $5 depending on how close the final predictions are to students' actual performances.
        '''.strip().replace('\n', '').replace('\t', '')

        submitted_attention_statement = submitted_form.get(
            'important-check').strip().replace('\n', '')

        error_message = None

        if attention_statement.lower().replace(' ', '') != submitted_attention_statement.lower().replace(' ', ''):
            error_message = 'Please enter the underlined text as is. You might be missing a word or some punctuation!'

        if error_message:
            page_params = {
                'error_message': error_message,
                'submitted_attention_statement': submitted_attention_statement,
                'user_group': survey_response.user_group,
            }

            return render(request, 'understand-payment-structure.html', page_params)

        survey_response.passed_second_attention_check = True
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
            'user_group': survey_response.user_group,
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

        if attention_statement.lower().replace(' ', '') == submitted_attention_statement.lower().replace(' ', ''):
            # Attention check passed
            survey_response.passed_first_attention_check = True
            survey_response.save()

            return HttpResponseRedirect(reverse('mech_task_choose_bonus'))

        error_message = 'Please enter the underlined text as is. You might be missing a word or some punctuation!'

        page_params = {
            'attention_text': survey_response.user_group.attention_check_statement,
            'error_message': error_message,
            'submitted_attention_statement': submitted_attention_statement,
            'user_group': survey_response.user_group,
        }

        return render(request, 'attention-check.html', page_params)


class ChooseBonusView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if survey_response.chose_bonus_baseline:
            return HttpResponseRedirect(reverse('mech_task_survey_question'))

        page_params = {
            'user_group': survey_response.user_group
        }

        return render(request, 'choose-bonus.html', page_params)

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if survey_response.user_group.use_freely:
            survey_response.use_model_estimates_for_bonus_calc = True
        else:
            submitted_form = request.POST

            error_message = None

            bonus_choice = submitted_form.get('bonus_preference').strip()
            if bonus_choice not in ['model', 'self']:
                error_message = 'Please select your bonus preference.'

            if error_message:
                page_params = {
                    'error_message': error_message, 'submitted_attention_statement': submitted_attention_statement, }

                return render(request, 'choose-bonus.html', page_params)

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
            elif selected_algo.startswith('kneighbors'):
                model_estimate_field = 'kneighbors_prediction'

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

        use_model_for_bonus = False

        if survey_response.user_group.use_model_estimates_only:
            if survey_response.use_model_estimates_for_bonus_calc:
                use_model_for_bonus = True

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

    def get_attrs(self, sample, attributes_to_show):

        attrs = OrderedDict()

        for attr_class in STUDENT_ATTRIBUTES:
            attrs[attr_class] = []

            for attr in STUDENT_ATTRIBUTES[attr_class]:
                if attributes_to_show != 'all':
                    if attr['attr_id'] not in attributes_to_show:
                        continue

                tmp = {
                    'text_to_show': attr['text_to_show'],
                    'attr_id': attr['attr_id'],
                    'description': attr['description'],
                }

                value = getattr(sample, attr['attr_id'])

                tmp['value'] = value

                if value == True:
                    if attr['attr_id'] == 'male':
                        tmp['value'] = 'Male'
                    else:
                        tmp['value'] = 'Yes'
                elif value == False:
                    if attr['attr_id'] == 'male':
                        tmp['value'] = 'Female'
                    else:
                        tmp['value'] = 'No'

                attrs[attr_class].append(tmp)

        return attrs

    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if survey_response.survey_estimates.count() == 0:
            self.assign_questions(survey_response)

        no_of_estimates_done = survey_response.number_of_estimates_done

        try:
            # Get one question from the allotted questions
            question = survey_response.survey_estimates.filter(completed=False)[
                0]
        except IndexError:
            # There are no more questions
            self.calculate_bonus(survey_response)
            return HttpResponseRedirect(reverse('mech_task_follow_up_questions'))

        # Build the attributes dict for the question
        sample = question.sample

        page_params = {
            'question': question,
            'sample': question.sample,
            'use_model_estimates_for_bonus_calc': survey_response.use_model_estimates_for_bonus_calc,
            'estimate_number': no_of_estimates_done + 1,
            'attributes': self.get_attrs(sample, survey_response.user_selected_attributes),
            'use_only_model_estimates_for_bonus_calc': survey_response.user_group.use_model_estimates_only,
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

        # Handle the case of accepting user estimates only if the estimates are
        # Within a 10 percentile range

        if survey_response.user_group.only_10_percentile_change:
            if survey_response.use_model_estimates_for_bonus_calc:
                lower_estimate = question.model_estimate - 10
                upper_estimate = question.model_estimate + 10

                if lower_estimate < 0:
                    lower_estimate = 0

                if upper_estimate > 100:
                    upper_estimate = 100

                lower_estimate = round(lower_estimate,0)
                upper_estimate = round(upper_estimate,0)

                if float(user_estimate) < lower_estimate or float(user_estimate) > upper_estimate:
                    error_message = 'Your estimate should be within %s and %s' % (
                        str(lower_estimate), str(upper_estimate))

                    no_of_estimates_done = survey_response.number_of_estimates_done
                    sample = question.sample

                    page_params = {
                        'question': question,
                        'sample': question.sample,
                        'use_model_estimates_for_bonus_calc': survey_response.use_model_estimates_for_bonus_calc,
                        'estimate_number': no_of_estimates_done + 1,
                        'attributes': self.get_attrs(sample, survey_response.user_selected_attributes),
                        'use_only_model_estimates_for_bonus_calc': survey_response.user_group.use_model_estimates_only,
                        'error_message': error_message,
                    }

                    return render(request, 'survey.html', page_params)

        question.user_estimate = float(user_estimate)
        question.completed = True
        question.save()

        survey_response.number_of_estimates_done += 1
        survey_response.save()

        return HttpResponseRedirect(reverse('mech_task_survey_question'))


class FollowUpQuestionsView(View):
    def get_list_of_attrs_to_show(self, selected_attrs):
        to_return = []

        for attr_class in STUDENT_ATTRIBUTES:
            for attr in STUDENT_ATTRIBUTES[attr_class]:
                if attr['attr_id'] in selected_attrs:
                    to_return.append('- ' + attr['text_to_show'])

        return to_return

    def get_next_question(self, survey_response):
        follow_up_questions = OrderedDict({
            'model_estimate_average_error': {
                # 'heading_text': 'Average error of the model',
                'question_text': 'On average, how many points do you think the model’s predictions are away from students’ actual performances',
                'sub_texts': ['An answer of 0 would mean that you think the model perfectly predicts all students\' performances. An answer of 23 would mean that you think the model’s predictions are off by 23 point on average.'],
                'type': 'number_input',
                'label': 'Enter your answer (0-100)',
            },
            'self_estimate_average_error': {
                # 'heading_text': 'Average error of your estimates',
                'question_text': 'On average, how many points do you think your predictions are away from students’ actual performances?',
                'sub_texts': ['An answer of 0 would mean that you think you perfectly predicts all students\' performances. An answer of 23 would mean that you think the model’s predictions are off by 23 point on average.'],
                'type': 'number_input',
                'label': 'Enter your answer (0-100)',
            },
            'model_estimate_confidence': {
                # 'heading_text': 'Confidence in the model\'s estimates',
                'question_text': 'How much confidence do you have in the statistical model’s predictions?',
                'type': 'likert',
                'scale': ['None', 'Little', 'Some', 'A Fair Amount', 'A Lot'],
            },
            'self_estimate_confidence': {
                # 'heading_text': 'Confidence in your estimates',
                'question_text': 'How much confidence do you have in your predictions?',
                'type': 'likert',
                'scale': ['None', 'Little', 'Some', 'A Fair Amount', 'A Lot'],
            },
            'why_chose_the_attributes': {
                'question_text': 'Why did you choose to use following factors to make your predictions?',
                'sub_texts': self.get_list_of_attrs_to_show(survey_response.user_selected_attributes),
                'type': 'long_text',
            },
            'why_chose_the_algorithm': {
                'question_text': 'Why did you choose to use %s to make your predictions regardless you ended up using it or not?' % (survey_response.user_selected_algorithm.name),
                'type': 'long_text',
            },
            'why_chose_model_estimate': {
                'question_text': 'Why did you choose to have your bonus be determined by the statistical model’s predictions instead of your predictions?',
                'type': 'long_text',
            },
            'why_chose_self_estimate': {
                'question_text': 'Why did you choose to have your bonus be determined by your predictions instead of the statistical model’s predictions?',
                'type': 'long_text',
            },
            'representativeness': {
                'question_text': 'How well do you think the model represent your assessment of the students’ performance?',
                'type': 'likert',
                'scale': ['Not representative at all', 'Slightly representative', 'Moderately representative', 'Very representative', 'Extremely representative'],
            },
            'transparency': {
                'question_text': 'How transparent would you rate the model’s prediction process? ',
                'type': 'likert',
                'scale': ['Not at all transparent', 'Slightly transparent', 'Moderately transparent', 'Very transparent', 'Extremely transparent'],
            },
            'fairness_questions': {
                'type': 'likert-set',
                'question_text': None,
                'questions': [
                    {
                        'question_id': 'fairness_tutoring_resources',
                        'question_text': 'Based on the scenarios you rated, would it be fair for the school to allocate tutoring resources to the students that the model predicts will have the lowest reading scores?',
                        'scale': ['Not at all fair', 'Slightly fair', 'Moderately fair', 'Very fair', 'Extremely fair'],
                    }, {
                        'question_id': 'fairness_scholarship',
                        'question_text': 'Based on the scenarios you rated, would it be fair for the school to recommend students with the highest predicted reading scores for a competitive scholarship in reading? ',
                        'scale': ['Not at all fair', 'Slightly fair', 'Moderately fair', 'Very fair', 'Extremely fair'],
                    },
                    {
                        'question_id': 'fairness_absent_students',
                        'question_text': 'Based on the scenarios you rated, would it be fair for the school to use the statistical model’s predictions to decide some part of the students’ final grade if the students were unable to attend exams?',
                        'scale': ['Not at all fair', 'Slightly fair', 'Moderately fair', 'Very fair', 'Extremely fair'],
                    },
                ],
                'explanation': {
                    'question_id': 'fairness_explanation',
                    'question_text': 'Please give a brief explanation for your choices to the three questions above',
                }
            },

            'likeliness_to_use_model': {
                'question_text': 'How likely would you be to use the model’s predictions to complete this task in the future?',
                'type': 'likert',
                'scale': ['Very unlikely', 'unlikely', 'undecided', 'likely', 'very likely'],
            },
            'any_other_thoughts': {
                'question_text': 'Do you have any other thoughts and feelings about the model? ',
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
            'fairness_questions',
            'fairness_tutoring_resources',
            'fairness_scholarship',
            'fairness_absent_students',
            'fairness_explanation',
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

            if survey_response.user_group.use_freely:
                # User didn't really have a choice to choose bonus structure
                if question in ['why_chose_model_estimate']:
                    continue

            if not survey_response.user_group.can_change_attributes:
                # User can't change attributes. So skip the related question
                if question in ['why_chose_the_attributes']:
                    continue

            if not survey_response.user_group.can_change_algorithm:
                # User can't select algorithm. So skip the related question
                if question in ['why_chose_the_algorithm']:
                    continue

            # A small hack around the group of likerts we have for fairness
            if question == 'fairness_questions':
                answer = getattr(
                    survey_response, 'fairness_tutoring_resources')
            else:
                answer = getattr(survey_response, question)

            if answer:
                continue

            if follow_up_questions[question]['type'] == 'number_input':
                if answer != None:
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

        if 'heading_text' in question_details:
            question_heading = question_details['heading_text']
        else:
            question_heading = None
        question_text = question_details['question_text']
        question_type = question_details['type']

        page_params = {
            'id': question,
            'text': question_text,
            'type': question_type,
            'heading': question_heading,
        }

        if 'sub_texts' in question_details:
            page_params['subs'] = question_details['sub_texts']

        if 'scale' in question_details:
            page_params['scale'] = question_details['scale']

        if 'label' in question_details:
            page_params['label'] = question_details['label']

        if 'questions' in question_details:
            page_params['questions'] = question_details['questions']

        if 'explanation' in question_details:
            page_params['explanation'] = question_details['explanation']

        return render(request, 'questions/' + question_type + '.html', page_params)

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        question_id = request.POST.get('question_id')

        if question_id.strip() == 'fairness_questions':
            fairness_questions = [
                'fairness_tutoring_resources',
                'fairness_scholarship',
                'fairness_absent_students',
                'fairness_explanation',
            ]

            for q_id in fairness_questions:
                answer = getattr(survey_response, q_id)

                if not answer:
                    setattr(survey_response, q_id,
                            request.POST.get('answer-' + q_id))

        else:
            answer = getattr(survey_response, question_id)

            if not answer:
                setattr(survey_response, question_id,
                        request.POST.get('answer').strip())

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
            'pronoun': {
                'question_text': 'What are your pronouns?',
                'options': ['He/his', 'She/her', 'They/their', 'Ze/zir','None of the above','I prefer not to answer']
            },
            'race': {
                'question_text': 'How do you identify your race?',
                'options': ['White', 'Black or African American', 'Asian', 'American Indian or Alaska Native', 'Middle Eastern or North African', 'Native Hawaiian or other pacific islander', 'Multi', 'None of the above', 'I prefer not to answer']
            },
            'ethnicity': {
                'question_text': 'How do you identify your ethnicity?',
                'options': ['Hispanic or Latino', 'Not Hispanic or Latino', 'I prefer not to answer']
            },
            'confidence_in_math': {
                'question_text': 'How would you rate your level of confidence in math?',
                'options': ['Not confident', ' Slightly confident', 'Confident', 'Very confident', 'Extremely confident']
            },
            'education': {
                'question_text': 'What is the highest level of education you have completed?',
                'options': ['Less than high school', 'High school/GED', 'Some college', '2-year college degree', '4-year college degree', 'Masters degree', 'Professional degree(JD, MD)', 'Doctoral degree', 'I prefer not to answer']
            },
            # 'prev_mturk_algo_participation': {
            #     'question_text': 'Have you participated in algorithm-related studies on Amazon Mechanical turk before?',
            #     'options': ['Yes', 'No']
            # },
        }

        return render(request, 'exit-survey.html', {'questions': exit_survey_questions})

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        survey_response.age = request.POST.get('age')
        survey_response.pronoun = request.POST.get('pronoun')
        survey_response.race = request.POST.get('race')
        survey_response.ethnicity = request.POST.get('ethnicity')
        survey_response.confidence_in_math = request.POST.get(
            'confidence_in_math')
        survey_response.prev_mturk_algo_participation_number = request.POST.get(
            'prev_mturk_algo_participation_number')
        survey_response.highest_level_of_education = request.POST.get(
            'education')

        user_ans = request.POST.get('att_check')

        # answer is True so it's equivalent to understood instruction
        survey_response.user_last_instruction_ans = user_ans

        survey_response.mturk_id_attempt_2 = request.POST.get(
            'final_mturk_id').strip()

        if survey_response.mturk_id_attempt_1.strip() == survey_response.mturk_id_attempt_2.strip():
            survey_response.final_mturk_id = survey_response.mturk_id_attempt_1.strip()
        else:
            # Save the responses first
            survey_response.save()

            return HttpResponseRedirect(reverse('mech_task_choose_mturk_id'))

        survey_response.completed = True
        survey_response.save()

        return HttpResponseRedirect(reverse('mech_task_thanks'))


class ChooseFinalMTurkIDView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if survey_response.final_mturk_id:
            return HttpResponseRedirect(reverse('mech_task_thanks'))

        page_params = {
            'mturk_id_1': survey_response.mturk_id_attempt_1,
            'mturk_id_2': survey_response.mturk_id_attempt_2,
        }

        return render(request, 'choose-mturk-id.html', page_params)

    def post(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        survey_response = request.user.mech_task_survey_response

        if survey_response.final_mturk_id:
            return HttpResponseRedirect(reverse('mech_task_thanks'))

        survey_response.final_mturk_id = request.POST.get('final_mturk_id')
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
            'user_group': survey_response.user_group,
        }

        return render(request, 'thanks.html', page_params)
