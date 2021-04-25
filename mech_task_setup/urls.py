from django.urls import path

from . import views

urlpatterns = [
    path('setup-mech-task', views.SetupMechTaskView.as_view(), name='setup_mech_task')
]
