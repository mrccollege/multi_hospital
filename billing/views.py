from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from accounts.models import CustomUser
from billing.models import PatientBillHistory
from patient_report.models import HeaderPatient, DetailsPatient
from store.models import MiniStore


def mini_store_login(request):
    if request.method == 'POST':
        form = request.POST
        username = form.get('email')
        password = form.get('password')

        username = username.strip()
        username = 'MRC Mini Store'
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
                return redirect('/billing/')
        else:
            error_message = "Invalid username or password"
    return render(request, 'mini_medical_store_login.html')


def mini_store_logout(request):
    logout(request)
    return redirect('/billing/login/')


@login_required(login_url='/billing/login/')
def patient_billing_list(request):
    mini_medical_user_id = request.session['mini_medical_user_id']
    mini_medical_details = MiniStore.objects.get(mini_store_user_id=mini_medical_user_id)
    hospital_id = mini_medical_details.hospital_id
    patient_bill = HeaderPatient.objects.filter(appointment__hospital_id=hospital_id)
    context = {
        'patient_bill': patient_bill,
    }
    return render(request, 'patient_billing_list.html', context)


def generate_bill(request, id):
    details = DetailsPatient.objects.filter(header_id=id)
    header = HeaderPatient.objects.get(head_id=id)
    context = {
        'header': header,
        'details': details,
    }
    return render(request, 'generate_bill.html', context)


def bill_generated(request, id=0):
    if request.method == 'POST':
        form = request.POST
        medicine_ids = form.getlist('medicine_id')
        patient_id = form.get('patient_id')
        hospital_id = form.get('hospital_id')
        doctor_id = form.get('doctor_id')
        qty = form.getlist('qty')
        price = form.getlist('price')
        cash_amount = form.get('cash_amount')
        online_amount = form.get('online_amount')
        remaining_amount = form.get('remaining_amount')
        g_amount = form.get('g_amount')
        if id == 0:
            history = PatientBillHistory.objects.create(medicine=medicine_ids,
                                                        qty=qty,
                                                        price=price,
                                                        patient=patient_id,
                                                        hospital=hospital_id,
                                                        doctor=doctor_id,
                                                        grand_total=g_amount,
                                                        cash=cash_amount,
                                                        online=online_amount,
                                                        remaining=remaining_amount,
                                                        )
            if history:
                msg = 'Bill Successfully Generated'
            else:
                msg = 'Bill Generated Failed!'
        else:
            pass
        context = {
            'msg': msg
        }
        return JsonResponse(context)
