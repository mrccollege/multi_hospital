from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from site_settings.models import LookupField
from store.models import MainStore, MiniStore
from .models import CustomUser, HospitalUser, DoctorUser, PatientUser, SocialMediaReference, OtherReference


def hospital_registration(request):
    if request.method == 'POST':
        form = request.POST
        full_name = form.get('hospitalName')
        email = form.get('email')
        password = form.get('password')
        address = form.get('address')
        mobile = form.get('contactNumber')
        user_type = 'HOSPITAL'
        user = CustomUser.objects.create_user(full_name=full_name,
                                              username=email,
                                              email=email,
                                              password=password,
                                              address=address,
                                              mobile=mobile,
                                              user_type=user_type,
                                              )
        if user:
            obj = HospitalUser.objects.create(user_id=user.id)
            if obj:
                return redirect('/accounts/hospital-login/')

    return render(request, 'hospital_user.html')


def hospital_login(request):
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
            if user.user_type == 'HOSPITAL':
                user = authenticate(username=username, password=password)
                login(request, user)
                request.session['hospital_user_id'] = user.id
                return redirect('/dashboard/hospital/')
        else:
            error_message = "Invalid username or password"

    else:
        return render(request, 'hospital_login.html')


def user_logout(request):
    logout(request)
    return redirect('/')


def doctor_registration(request):
    if request.method == 'POST':
        hospital_user_id = request.session.get('hospital_user_id')
        if hospital_user_id is None:
            return redirect('/accounts/hospital-login/')
        form = request.POST
        full_name = form.get('doctorName')
        full_name = full_name.title()
        specialization = form.get('specialization')
        specialization = specialization.title()
        degree = form.get('degree')
        degree = degree.upper()
        email = form.get('email')
        password = form.get('password')
        address = form.get('address')
        mobile = form.get('contactNumber')
        user_type = 'DOCTOR'
        user = CustomUser.objects.create_user(full_name=full_name,
                                              username=email,
                                              email=email,
                                              password=password,
                                              address=address,
                                              mobile=mobile,
                                              specialization=specialization,
                                              degree=[degree],
                                              user_type=user_type,
                                              )
        if user:
            h_id = HospitalUser.objects.get(user_id=hospital_user_id)
            doctor = DoctorUser.objects.create(user_id=user.id, hospital_id=h_id.h_id)
            if doctor:
                return redirect('/dashboard/hospital/')
    else:
        hospital_user_id = request.session.get('hospital_user_id')
        if hospital_user_id is None:
            return redirect('/accounts/hospital-login/')
        else:
            return render(request, 'doctor_registration.html')



def add_reference(request):
    if request.method == 'POST':
        hospital_user_id = request.session.get('hospital_user_id')
        h_id = HospitalUser.objects.get(user_id=hospital_user_id)
        form = request.POST
        reference_name = form.get('reference_name')
        reference_address = form.get('reference_address')
        reference_mobile = form.get('reference_mobile')

        obj = OtherReference.objects.create(hospital_id=h_id.h_id,
                                            name=reference_name,
                                            address=reference_address,
                                            contact=reference_mobile)
        obj_data = {}
        if obj:
            status = 1

            obj_data['id'] = obj.id
            obj_data['name'] = obj.name
        else:
            status = 0

        context = {
            'status': status,
            'obj_data': obj_data,
        }
        return JsonResponse(context)


def get_patient_reference(request):
    hospital_user_id = request.session.get('hospital_user_id')
    h_id = HospitalUser.objects.get(user_id=hospital_user_id)
    if request.method == 'GET':
        form = request.GET
        search_value = form.get('search_value')
        patient = PatientUser.objects.filter(Q(hospital_id=h_id.h_id),
                                             Q(user__full_name__icontains=search_value)
                                             )
        patient_list = []
        for i in patient:
            data_dict = {}
            data_dict['id'] = i.p_id
            data_dict['name'] = i.user.full_name
            patient_list.append(data_dict)
        context = {
            'results': patient_list,
        }
        return JsonResponse(context)


def patient_registration(request):
    hospital_user_id = request.session.get('hospital_user_id')
    if hospital_user_id is None:
            return redirect('/accounts/hospital-login/')
    h_id = HospitalUser.objects.get(user_id=hospital_user_id)

    if request.method == 'POST':
        form = request.POST
        full_name = form.get('patientName')
        full_name = full_name.title()
        age = form.get('age')
        gender = form.get('gender')
        email = form.get('email')
        password = form.get('password')
        address = form.get('address')
        address = address.title()
        mobile = form.get('contactNumber')
        user_type = 'PATIENT'
        social_ref = form.get('social_ref')
        other_ref = form.get('other_ref')
        patient_ref = form.get('patient_reference_id')

        if social_ref:
            social_ref = social_ref
        else:
            social_ref = None

        if other_ref:
            other_ref = other_ref
        else:
            other_ref = None

        if patient_ref:
            patient_ref = patient_ref
        else:
            patient_ref = None

        user = CustomUser.objects.create_user(full_name=full_name,
                                              username=email,
                                              age=age,
                                              gender=gender,
                                              email=email,
                                              password=password,
                                              address=address,
                                              mobile=mobile,
                                              user_type=user_type,
                                              )
        if user:
            patient = PatientUser.objects.create(user_id=user.id,
                                                 hospital_id=h_id.h_id,
                                                 social_ref_id=social_ref,
                                                 other_ref_id=other_ref,
                                                 patient_ref=patient_ref,
                                                 )
            if patient:
                return redirect('/dashboard/hospital/')
    else:
        social_ref = SocialMediaReference.objects.filter(hospital_id=h_id.h_id)
        other_ref = OtherReference.objects.filter(hospital_id=h_id.h_id)
        context = {
            'social_ref': social_ref,
            'other_ref': other_ref,
        }
        return render(request, 'patient_registration.html', context)


def main_medical_store_registration(request):
    if request.method == 'POST':
        form = request.POST
        medical_name = form.get('medicalName')
        medical_name = medical_name.title()
        email = form.get('email')
        password = form.get('password')
        user_type = 'MAIN_MEDICAL_STORE'
        user = CustomUser.objects.create_user(full_name=medical_name,
                                              username=email,
                                              email=email,
                                              password=password,
                                              user_type=user_type,
                                              )
        if user:
            hospital_user_id = request.session.get('hospital_user_id')
            h_id = HospitalUser.objects.get(user_id=hospital_user_id)
            obj = MainStore.objects.create(main_store_user_id=user.id, hospital_id=h_id.h_id)
            if obj:
                return redirect('/')

    return render(request, 'main_medical_store_register.html')


def main_medical_store_login(request):
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
            if user.user_type == 'MAIN_MEDICAL_STORE':
                user = authenticate(username=username, password=password)
                login(request, user)
                request.session['main_medical_user_id'] = user.id
                return redirect('/store/main_medical_store_dashboard/')
        else:
            error_message = "Invalid username or password"
    return render(request, 'main_medical_store_login.html')


def mini_medical_store_registration(request):
    if request.method == 'POST':
        form = request.POST
        medical_name = form.get('medicalName')
        medical_name = medical_name.title()
        email = form.get('email')
        password = form.get('password')
        user_type = 'MINI_MEDICAL_STORE'
        user = CustomUser.objects.create_user(full_name=medical_name,
                                              username=email,
                                              email=email,
                                              password=password,
                                              user_type=user_type,
                                              )
        if user:
            hospital_user_id = request.session.get('hospital_user_id')
            h_id = HospitalUser.objects.get(user_id=hospital_user_id)
            obj = MiniStore.objects.create(mini_store_user_id=user.id, hospital_id=h_id.h_id)
            if obj:
                return redirect('/')

    return render(request, 'mini_medical_store_register.html')


def mini_medical_store_login(request):
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
            if user.user_type == 'MINI_MEDICAL_STORE':
                user = authenticate(username=username, password=password)
                login(request, user)
                request.session['mini_medical_user_id'] = user.id
                return redirect('/store/mini_medical_store_dashboard/')
        else:
            error_message = "Invalid username or password"
    return render(request, 'mini_medical_store_login.html')
