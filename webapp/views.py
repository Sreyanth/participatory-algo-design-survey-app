import random
import uuid

from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect, render, reverse
from django.views import View

from .models import (MechTaskAlgorithm, MechTaskStudentSample,
                     MechTaskSurveyEstimate, MechTaskSurveyResponse,
                     MechTaskUserGroup)


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

        try:
            algorithm = MechTaskAlgorithm.objects.get(
                slug=request.POST.get('algorithm').strip())
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('mech_task_choose_attributes'))

        survey_response = request.user.mech_task_survey_response
        survey_response.algorithm = algorithm
        survey_response.save()

        return HttpResponseRedirect(reverse('mech_task_choose_attributes'))


class ChooseAttributesView(View):
    # TODO: Implement these methods
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

        return render(request, 'choose-attributes.html')

    def post(self, request):
        pass


class UnderstandModelView(View):
    def get(self, request):
        if user_fails_access_check(request):
            return HttpResponseRedirect(reverse('home_page'))

        return render(request, 'understand-model.html')

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

        return render(request, 'attention-check.html', {'attention_text': survey_response.user_group.attention_check_statement})

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
            survey_response.model_estimates_for_bonus_calc = True
        else:
            survey_response.model_estimates_for_bonus_calc = False

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
            pass

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
            return HttpResponseRedirect(reverse('mech_task_follow_up_questions'))

        return render(request, 'survey.html', {'question': question, 'sample': question.sample})

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

        return HttpResponseRedirect(reverse('mech_task_survey_question'))
