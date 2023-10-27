from django.http import JsonResponse
from django.shortcuts import render, redirect
from accounts.models import DoctorUser, PatientUser
from .models import PatientAppointment


# Create your views here.
def patient_appointment(request):
    if request.method == 'POST':
        form = request.POST
        hospital = 1
        patient_id = form.get('patientID')
        doctor_id = form.get('doctorID')
        appointment_date = form.get('appointmentDate')
        appointment_time = form.get('appointmentTime')
        blood_pressure = form.get('bloodPressure')
        weight = form.get('weight')
        print(doctor_id,'===========doctor_id')
        appoint = PatientAppointment.objects.create(hospital_id=hospital,
                                                    patient_id=patient_id,
                                                    doctor_id=doctor_id,
                                                    appointment_date=appointment_date,
                                                    appointment_time=appointment_time,
                                                    bloodPressure=blood_pressure,
                                                    weight=weight, )

        if appoint:
            return redirect('/appointment/patient-appointment/')
    doctor = DoctorUser.objects.filter()
    context = {
        'doctor': doctor
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
