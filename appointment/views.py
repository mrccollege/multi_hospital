import datetime

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
        return redirect('/accounts/hospital-login/')
    h_id = HospitalUser.objects.get(user_id=hospital_user_id)
    if request.method == 'POST':
        form = request.POST
        appoint_ward = form.get('appointment_ward')
        patient_id = form.get('patientID')
        doctor_id = form.get('doctorID')
        appointment_date = form.get('appointmentDate')
        blood_pressure = form.get('bloodPressure')
        pulse = form.get('pulse')
        weight = form.get('weight')
        paid_free = form.get('paid_free')
        cash = form.get('cash')
        online = form.get('online')
        remaining = form.get('remaining')
        ward_obj = HospitalAppointmentVisit.objects.filter(id=appoint_ward)
        if ward_obj:
            ward_price = ward_obj[0].price
        else:
            ward_price = None

        if appointment_date:
            appointment_date = appointment_date
        else:
            appointment_date = datetime.datetime.now().date()
        appoint = PatientAppointment.objects.create(hospital_id=h_id.h_id,
                                                    appoint_ward_id=appoint_ward,
                                                    patient_id=patient_id,
                                                    doctor_id=doctor_id,
                                                    appointment_date=appointment_date,
                                                    bloodPressure=blood_pressure,
                                                    weight=weight,
                                                    fees=ward_price,
                                                    pulses=pulse,
                                                    paid_free=paid_free,
                                                    cash=cash,
                                                    online=online,
                                                    remaining=remaining,
                                                    )

        if appoint:
            return redirect('/appointment/patient_appointment_list/')

    else:
        doctor = DoctorUser.objects.filter(hospital_id=h_id.h_id)
        ward = HospitalAppointmentVisit.objects.filter(hospital_id=h_id.h_id)
        context = {
            'doctor': doctor,
            'ward': ward,
        }
        return render(request, 'appointment.html', context)


def patient_search(request):
    hospital_user_id = request.session.get('hospital_user_id')
    if hospital_user_id is None:
        return redirect('/accounts/hospital-login/')
    h_id = HospitalUser.objects.get(user_id=hospital_user_id)
    term = request.GET.get('term', '')
    # Search for patients and doctors whose names contain the search term
    patient = PatientUser.objects.filter(user__full_name__icontains=term, hospital_id=h_id.h_id)
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


def get_ward_price(request):
    form = request.GET
    ward_id = form.get('ward_id')
    ward_obj = HospitalAppointmentVisit.objects.filter(id=ward_id)
    if ward_obj:
        ward_price = ward_obj[0].price
    context = {
        'ward_id': ward_id,
        'ward_price': ward_price,
    }
    return JsonResponse(context)
