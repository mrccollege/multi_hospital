from django.http import JsonResponse
from django.shortcuts import render, redirect
from accounts.models import DoctorUser, PatientUser, HospitalUser
from dashboard.models import HospitalAppointmentVisit
from .models import PatientAppointment


def patient_appointment_list(request):
    hospital_user_id = request.session.get('hospital_user_id')
    if hospital_user_id is None:
        return redirect('/accounts/hospital-login/')
    else:
        h_id = HospitalUser.objects.get(user_id=hospital_user_id)
        appoint = PatientAppointment.objects.filter(hospital_id=h_id.h_id, appoint_status='unchecked')
        context = {
            'appoint': appoint,
        }
    return render(request, 'appointment_list.html', context)


# Create your views here.
def patient_appointment(request):
    hospital_user_id = request.session.get('hospital_user_id')
    if hospital_user_id is None:
        redirect('/accounts/hospital-login/')
    h_id = HospitalUser.objects.get(user_id=hospital_user_id)
    if request.method == 'POST':
        form = request.POST
        appoint_ward = form.get('appointment_ward')
        patient_id = form.get('patientID')
        doctor_id = form.get('doctorID')
        appointment_date = form.get('appointmentDate')
        appointment_time = form.get('appointmentTime')
        blood_pressure = form.get('bloodPressure')
        weight = form.get('weight')
        appoint = PatientAppointment.objects.create(hospital_id=h_id.h_id,
                                                    appoint_ward_id=appoint_ward,
                                                    patient_id=patient_id,
                                                    doctor_id=doctor_id,
                                                    appointment_date=appointment_date,
                                                    appointment_time=appointment_time,
                                                    bloodPressure=blood_pressure,
                                                    weight=weight, )

        if appoint:
            return redirect('/appointment/patient_appointment_list/')

    else:
        doctor = DoctorUser.objects.filter()
        ward = HospitalAppointmentVisit.objects.filter(hospital_id=h_id.h_id)
        context = {
            'doctor': doctor,
            'ward': ward,
        }
        return render(request, 'appointment.html', context)


def patient_search(request):
    term = request.GET.get('term', '')
    # Search for patients and doctors whose names contain the search term
    patient = PatientUser.objects.filter(user__full_name__icontains=term)
    patient_data = []
    for i in patient:
        data_dict = {}
        data_dict['id'] = i.p_id
        data_dict['name'] = i.user.full_name
        data_dict['mobile'] = i.user.mobile
        patient_data.append(data_dict)

    context = {
        'results': patient_data,
    }
    return JsonResponse(context)


def doctor_search(request):
    term = request.GET.get('term', '')

    # Search for patients and doctors whose names contain the search term
    doctor = DoctorUser.objects.filter(user__full_name__icontains=term)

    doctor_data = []
    for i in doctor:
        data_dict = {}
        data_dict['id'] = i.d_id
        data_dict['name'] = i.user.full_name
        data_dict['degree'] = i.user.degree
        doctor_data.append(data_dict)

    context = {
        'results': doctor_data,
    }

    return JsonResponse(context)
