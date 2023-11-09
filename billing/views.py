from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from accounts.models import CustomUser
from billing.models import PatientBillHistory
from patient_report.models import HeaderPatient, DetailsPatient
from store.models import MiniStore

def mini_store_logout(request):
    logout(request)
    return redirect('/accounts/mini_medical_store_login/')


@login_required(login_url='/accounts/mini_medical_store_login/')
def patient_billing_list(request):
    mini_medical_user_id = request.session['mini_medical_user_id']
    mini_medical_details = MiniStore.objects.get(mini_store_user_id=mini_medical_user_id)
    hospital_id = mini_medical_details.hospital_id
    patient_bill = HeaderPatient.objects.filter(appointment__hospital_id=hospital_id, status='unbilled')
    context = {
        'patient_bill': patient_bill,
    }
    return render(request, 'patient_billing_list.html', context)


def generate_bill(request, head_id):
    header = HeaderPatient.objects.get(head_id=head_id)
    details = DetailsPatient.objects.filter(header_id=head_id)
    context = {
        'head_id': head_id,
        'header': header,
        'details': details,
    }
    # return render(request, 'generate_bill.html', context)
    return render(request, 'generate_bill1.html', context)


def generated_bill(request, id=0):
    if request.method == 'POST':
        form = request.POST
        medicine_ids = form.getlist('medicine_id')
        head_id = form.get('head_id')
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
            history = PatientBillHistory.objects.create(header_patient_id=head_id,
                                                        medicine=medicine_ids,
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
                header = HeaderPatient.objects.filter(head_id=head_id).update(status='billed')
                if header:
                    msg = 'Bill Successfully Generated'
            else:
                msg = 'Bill Generated Failed!'
        else:
            pass
        context = {
            'msg': msg
        }
        return JsonResponse(context)
