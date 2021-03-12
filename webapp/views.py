import random
import uuid

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect, render, reverse
from django.views import View

from .models import MechTaskSurveyResponse, MechTaskUserGroup


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class StartSurveyView(View):
    def create_a_new_user(self):
        new_user = User()
        new_user.username = uuid.uuid4()
        new_user.save()

        return new_user

    def create_survey_response(self, request):
        survey_response = MechTaskSurveyResponse()
        survey_response.user = request.user

        # Randomly assign a survey group
        # Right now, we fetch all groups all the time. We can optimize this.
        # TODO: optimize this workflow.
        survey_groups = MechTaskUserGroup.objects.all()
        random_survey_group = random.choice(survey_groups)

        survey_response.user_group = random_survey_group
        survey_response.save()

        return HttpResponseRedirect(reverse('mech_task_consent'))

    def get(self, request):
        if not request.user.is_authenticated:
            user = self.create_a_new_user()
            login(request, user)
            return self.create_survey_response(request)

        user = request.user

        try:
            survey_response = user.mech_task_survey_response
            return HttpResponseRedirect(reverse('mech_task_consent'))
        except ObjectDoesNotExist:
            return self.create_survey_response(request)


class ConsentView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home_page'))

        try:
            survey_response = request.user.mech_task_survey_response
            if survey_response.user_consented_to_survey:
                return HttpResponseRedirect(reverse('mech_task_instructions'))
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('home_page'))

        page_params = {
            'user': request.user,
        }

        return render(request, 'consent.html', page_params)

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home_page'))

        try:
            survey_response = request.user.mech_task_survey_response
            if survey_response.user_consented_to_survey:
                return HttpResponseRedirect(reverse('mech_task_instructions'))
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('home_page'))

        submitted_form = request.POST

        age_check = request.POST.get('age_check')
        consent_check = request.POST.get('consent_check')
        read_information_check = request.POST.get('read_information_check')

        mturk_id_1 = request.POST.get('mturk_id_1').strip()
        mturk_id_2 = request.POST.get('mturk_id_2').strip()

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
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home_page'))

        try:
            survey_response = request.user.mech_task_survey_response
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('home_page'))
        return render(request, 'instructions.html')

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home_page'))

        try:
            survey_response = request.user.mech_task_survey_response
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('home_page'))

        survey_response.read_first_instruction = True
        survey_response.read_percentile_description = True
        survey_response.save()

        return HttpResponseRedirect(reverse('mech_task_datapoints'))


class UnderstandDataView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home_page'))

        try:
            survey_response = request.user.mech_task_survey_response
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('home_page'))

        return render(request, 'understand-data.html')

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home_page'))

        try:
            survey_response = request.user.mech_task_survey_response
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('home_page'))

        survey_response.read_sample_data_points = True
        survey_response.save()

        return HttpResponseRedirect(reverse('mech_task_model'))


class UnderstandModelView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home_page'))

        try:
            survey_response = request.user.mech_task_survey_response
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('home_page'))

        return render(request, 'understand-model.html')

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home_page'))

        try:
            survey_response = request.user.mech_task_survey_response
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('home_page'))

        survey_response.read_model_description = True
        survey_response.read_that_model_is_off = True
        survey_response.save()

        return HttpResponseRedirect(reverse('attention_check_1'))


class SurveyView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home_page'))

        try:
            survey_response = request.user.mech_task_survey_response
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('home_page'))

        try:
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
            return HttpResponseRedirect(reverse('mech_task_survey'))

        question.user_estimate = float(user_estimate)
        question.completed = True
        question.save()

        return HttpResponseRedirect(reverse('mech_task_survey'))
