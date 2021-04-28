from django.urls import path

from . import views

urlpatterns = [
    path('create-linear-reg', views.CreateLinearRegressionView.as_view(),
         name='create_linear_regression'),
    path('get-test-user/<slug:slug>', views.GetTestUserView.as_view(),
         name='get_test_user')
]
