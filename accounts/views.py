from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from store.models import MainStore, MiniStore
from .models import CustomUser, HospitalUser, DoctorUser, PatientUser


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
                return redirect('/')
        else:
            error_message = "Invalid username or password"
    return render(request, 'hospital_login.html')


def user_logout(request):
    logout(request)
    return redirect('/')


def doctor_registration(request):
    if request.method == 'POST':
        form = request.POST
        full_name = form.get('doctorName')
        specialization = form.get('specialization')
        degree_list = []

        degree = form.get('specialization')
        degree_list.append(degree)
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
                                              degree=degree_list,
                                              user_type=user_type,
                                              )
        if user:
            hospital_user_id = request.session.get('hospital_user_id')
            h_id = HospitalUser.objects.get(user_id=hospital_user_id)
            DoctorUser.objects.create(user_id=user.id, hospital_id=h_id.h_id)
            return redirect('/')

    else:
        hospital_user_id = request.session.get('hospital_user_id')
        return render(request, 'doctor_user.html')


def patient_registration(request):
    if request.method == 'POST':
        form = request.POST
        full_name = form.get('patientName')
        age = form.get('age')
        gender = form.get('gender')
        email = form.get('email')
        password = form.get('password')
        address = form.get('address')
        mobile = form.get('contactNumber')
        user_type = 'PATIENT'
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
            hospital_user_id = request.session.get('hospital_user_id')
            h_id = HospitalUser.objects.get(user_id=hospital_user_id)
            PatientUser.objects.create(user_id=user.id, hospital_id=h_id.h_id)
            return redirect('/')

    return render(request, 'patient_user.html')


def main_medical_store_registration(request):
    if request.method == 'POST':
        form = request.POST
        medical_name = form.get('medicalName')
        username = form.get('username')
        email = form.get('email')
        password = form.get('password')
        user_type = 'MAIN_MEDICAL_STORE'
        user = CustomUser.objects.create_user(full_name=medical_name,
                                              username=username,
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


def mini_medical_store_registration(request):
    if request.method == 'POST':
        form = request.POST
        medical_name = form.get('medicalName')
        username = form.get('username')
        email = form.get('email')
        password = form.get('password')
        user_type = 'MINI_MEDICAL_STORE'
        user = CustomUser.objects.create_user(full_name=medical_name,
                                              username=username,
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
