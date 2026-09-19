from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('donor/', views.donor, name='donor'),
    path('patient/', views.patient, name='patient'),
    path('blood_search/', views.blood_search, name='blood_search'),
    path('blood-request/', views.blood_request, name='blood_request'),
    path('login/', views.login_view, name='Login'),
]