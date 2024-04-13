# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Appointment



class AppointmentForm(forms.ModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={'id': 'datepicker', 'placeholder': 'Select Date'}))
    time = forms.TimeField(widget=forms.TextInput(attrs={'id': 'timepicker', 'placeholder': 'Select Time'}))

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'doctor']
class DoctorRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name')

class PatientRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)))
    class Meta:
       model = CustomUser
       fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth', 'is_patient')
       labels = {'is_patient': 'Are you a patient?'}

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('patient', 'Patient'), ('doctor', 'Doctor')])