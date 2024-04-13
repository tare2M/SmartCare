from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import DoctorRegistrationForm, PatientRegistrationForm,UserLoginForm,AppointmentForm
from django.shortcuts import render
from .models import Doctor, Patient,Appointment
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .chat import chatbot_response  # Import your chatbot function
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .chat import get_response

def error_404(request, exception):
    return render(request, '404.html', status=404)
def error_500(request):
    return render(request, '500.html', status=500)




def home(request):
    return render(request, 'home.html')
def chat(request):
    return render(request, 'chat.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')


def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_doctor = True
            user.save()
            # Create and link a Doctor object
            doctor = Doctor(user=user)
            doctor.save()
            # Log the user in
            login(request, user)
            return redirect('doctor_profile')
        else:
            # Form validation failed, display error alert
            messages.error(request, 'Failed to create patient account. Please check the entered information.')
            return render(request, 'doctor/doctor_signup.html', {'form': form, 'show_alert': True})
    else:
        form = DoctorRegistrationForm()
    return render(request, 'doctor/doctor_signup.html', {'form': form})

def patient_signup(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_patient = True
            user.save()

            # Extract and save date_of_birth
            date_of_birth = form.cleaned_data['date_of_birth']

            # Create a Patient object with the date_of_birth
            patient = Patient(user=user, date_of_birth=date_of_birth)
            patient.save()

            # Log the user in
            login(request, user)
            return redirect('patient_profile')
        else:
            # Form validation failed, display error alert
            messages.error(request, 'Failed to create patient account. Please check the entered information.')
            return render(request, 'patient/patient_signup.html', {'form': form, 'show_alert': True})
    else:
        form = PatientRegistrationForm()
    return render(request, 'patient/patient_signup.html', {'form': form, 'show_alert': False})


@login_required
def doctor_profile(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        # Handle the case where a Doctor object does not exist
        # Redirect the user to an appropriate page or show an error message
        return render(request, 'doctor/doctor_not_found.html')
    appointments = Appointment.objects.filter(doctor=doctor)
    return render(request, 'doctor/doctor_profile.html', {'doctor': doctor,'appointments': appointments})

@login_required
def patient_profile(request):
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        # Handle the case where a patient object does not exist
        # Redirect the user to an appropriate page or show an error message
        return render(request, 'patient/patient_not_found.html')

    appointments = Appointment.objects.filter(patient=patient)

    # Chatbot logic
    chat_history = []
    if request.method == 'POST':
        user_message = request.POST.get('user_message')
        chat_history.append({'user': True, 'text': user_message})
        chatbot_response_text = chatbot_response(user_message)
        chat_history.append({'user': False, 'text': chatbot_response_text})

    return render(request, 'patient/patient_profile.html', {'patient': patient, 'appointments': appointments, 'chat_history': chat_history})
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if role == 'patient':
                    return redirect('patient_profile')
                elif role == 'doctor':
                    return redirect('doctor_profile')
            else:
                # Invalid login attempt
                messages.error(request, 'Invalid username or password')
                return render(request, 'login.html', {'form': form, 'show_alert': True})  # Pass show_alert=True to trigger alert in template
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form, 'show_alert': False})
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient  # Assuming you have a patient profile linked to users
            appointment.save()
            messages.success(request, 'Appointment booked successfully.')
            return redirect('patient_profile')
    else:
        form = AppointmentForm()
    return render(request, 'patient/book_appointment.html', {'form': form})

@login_required
def patient_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user.patient)
    return render(request, 'patient/patient_profile.html', {'appointments': appointments})

@login_required
def doctor_schedule(request):
    if request.user.is_doctor:
        appointments = Appointment.objects.filter(doctor=request.user.doctor)
        return render(request, 'doctor/doctor_profile.html', {'appointments': appointments})
    else:
        return render(request, 'error.html', {'message': 'You are not authorized to access this page.'})


