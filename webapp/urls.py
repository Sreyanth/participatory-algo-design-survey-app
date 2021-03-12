from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home_page'),
    path('start', views.StartSurveyView.as_view(), name='start_mech_task_survey'),
    path('consent', views.ConsentView.as_view(), name='mech_task_consent'),
    path('instructions', views.InstructionsView.as_view(),
         name='mech_task_instructions'),
    path('understand-data', views.UnderstandDataView.as_view(),
         name='mech_task_datapoints'),
    path('understand-model', views.UnderstandModelView.as_view(),
         name='mech_task_model'),
    path('survey', views.SurveyView.as_view(),
         name='mech_task_survey'),
]
