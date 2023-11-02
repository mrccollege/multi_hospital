from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
from accounts.models import CustomUser
from appointment.models import PatientAppointment


@login_required(login_url='/doctor/login/')
def doctor_dashboard(request):
    user_id = request.session['user_id']
    if user_id:
        appoint = PatientAppointment.objects.filter(doctor__user_id=user_id)
        context = {
            'appoint': appoint
        }
        return render(request, 'doctor_dashboard.html', context)


def doctor_login(request):
    if request.method == 'POST':
        form = request.POST
        username = form.get('email')
        password = form.get('password')

        username = username.strip()
        password = password.strip()
        user = CustomUser.objects.filter(username=username).first()
        # user = authenticate(username=username, password=password)
        # if user is not None:
        if user is not None and user.check_password(password):
            if user.user_type == 'DOCTOR':
                login(request, user)  # Log the user in
                request.session['user_id'] = user.id
                return redirect('/doctor/dashboard/')

        # user = authenticate(username=username, password=password)
        # if user is not None:
        #     if user.user_type == 'DOCTOR':
        #         login(request, user)  # Log the user in
        #         request.session['user_id'] = user.id
        #         return redirect('/doctor/dashboard/')
        else:
            error_message = "Invalid username or password"
    return render(request, 'doctor_login.html')


def doctor_logout(request):
    logout(request)
    return redirect('/doctor/login/')


def patient_report(request, appointment_id):
    appoint = PatientAppointment.objects.get(patient_appoint_id=appointment_id)
    context = {
        'appoint': appoint,
    }
    return render(request, 'patient_details.html', context)
