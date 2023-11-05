from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
from accounts.models import CustomUser, DoctorUser
from appointment.models import PatientAppointment
from patient_report.models import HeaderPatient, DetailsPatient


@login_required(login_url='/doctor/login/')
def doctor_dashboard(request):
    doctor_user_id = request.session['doctor_user_id']
    if doctor_user_id:
        doctor_details = DoctorUser.objects.get(user_id=doctor_user_id)
        appoint = PatientAppointment.objects.filter(doctor__user_id=doctor_user_id)
        context = {
            'hospital_id': doctor_details.hospital.h_id,
            'doctor_details': doctor_details,
            'appoint': appoint
        }
        return render(request, 'doctor_dashboard.html', context)
    else:
        return redirect('/doctor/login/')


def doctor_login(request):
    if request.method == 'POST':
        form = request.POST
        username = form.get('email')
        password = form.get('password')

        username = username.strip()
        password = password.strip()
        try:
            user = CustomUser.objects.filter(username=username).first()
        except Exception as e:
            print(e, '===========e==========')
            user = None

        if user is not None:
            if user.user_type == 'DOCTOR':
                user = authenticate(username=username, password=password)
                login(request, user)
                request.session['doctor_user_id'] = user.id
                return redirect('/doctor/dashboard/')
        else:
            error_message = "Invalid username or password"
    return render(request, 'doctor_login.html')


def doctor_logout(request):
    logout(request)
    return redirect('/doctor/login/')


def patient_report(request, appointment_id):
    if request.method == 'POST':
        form = request.POST
        disease = form.get('disease')
        medicine_id = form.getlist('medicine_id')
        dosage = form.getlist('dosage')
        frequency = form.getlist('frequency')
        print(disease, '===============disease')
        print(medicine_id, '===============medicine_id')

        head = HeaderPatient.objects.create(appointment_id=appointment_id,
                                            disease=disease,
                                            )
        if head:
            for i in range(len(medicine_id)):
                if medicine_id[i]:
                    DetailsPatient.objects.create(header_id=head.head_id,
                                                  medicine_details_id=medicine_id[i],
                                                  dosage=dosage[i],
                                                  frequency=frequency[i],
                                                  )
            msg = 'saved successfully.'
            context = {
                'appointment_id': appointment_id,
                'msg': msg,
            }
            return JsonResponse(context)
    else:
        appoint = PatientAppointment.objects.get(patient_appoint_id=appointment_id)
        context = {
            'appointment_id': appointment_id,
            'appoint': appoint,
        }
        return render(request, 'patient_report.html', context)
