from django.urls import path
from . import views

handler500 = 'users.views.error_500'
handler404 = 'users.views.error_404'
urlpatterns = [
    # Add the URL pattern for the homepage
    path('', views.home, name='home'),

    path('doctor/signup/', views.doctor_signup, name='doctor_signup'),
    path('patient/signup/', views.patient_signup, name='patient_signup'),
    path('doctor/profile/', views.doctor_profile, name='doctor_profile'),
    path('patient/profile/', views.patient_profile, name='patient_profile'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('patient/book_appointment/', views.book_appointment, name='book_appointment'),
    path('doctor_schedule/', views.doctor_schedule, name='doctor_schedule'),




]
