from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home_page'),
    path('start', views.StartSurveyView.as_view(),
         name='start_mech_task_survey'),
    path('consent', views.ConsentView.as_view(), name='mech_task_consent'),
    path('instructions', views.InstructionsView.as_view(),
         name='mech_task_instructions'),
    path('understand-data', views.UnderstandDataView.as_view(),
         name='mech_task_understand_datapoints'),
    path('choose-algorithm', views.ChooseAlgorithmView.as_view(),
         name='mech_task_choose_algorithm'),
    path('choose-algorithm-attributes', views.ChooseAttributesView.as_view(),
         name='mech_task_choose_attributes'),
    path('understand-model', views.UnderstandModelView.as_view(),
         name='mech_task_understand_model'),
    path('understand-payment-structure', views.UnderstandPaymentStructureView.as_view(),
         name='mech_task_understand_payment_structure'),
    path('pre-survey-confirmation', views.AttentionCheckView.as_view(),
         name='mech_task_attention_check'),
    path('choose-bonus-structure', views.ChooseBonusView.as_view(),
         name='mech_task_choose_bonus'),
    path('survey', views.SurveyView.as_view(),
         name='mech_task_survey_question'),
    path('post-survey-questions', views.FollowUpQuestionsView.as_view(),
         name='mech_task_follow_up_questions'),
    path('exit-survey', views.ExitSurveyView.as_view(),
         name='mech_task_exit_survey'),
    path('thanks', views.ThanksView.as_view(),
         name='mech_task_thanks'),
]
