from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from accounts.models import Stores
from site_settings.models import LookupField
from store.models import MainStoreMedicine, MiniStoreMedicine
from .models import PatientBillHistoryHead, PatientBillHistoryDetails
from patient_report.models import HeaderPatient, DetailsPatient

import os

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import EmailMessage
from xhtml2pdf import pisa


def generate_pdf(html_content, output_path):
    """
    Generate a PDF file from HTML content and save it to the specified path using pisa.
    """
    with open(output_path, 'w+b') as pdf_file:
        pisa.CreatePDF(html_content, dest=pdf_file)


def send_pdf_email(bill_history_id):
    # Your email template data
    header = PatientBillHistoryHead.objects.get(head_id=bill_history_id)
    details = PatientBillHistoryDetails.objects.filter(head_id=bill_history_id)
    context = {
        'header': header,
        'details': details,
    }
    # Render the HTML template with the data
    html_content = render_to_string('email_template.html', context)

    # Generate a temporary PDF file
    pdf_output_path = 'output.pdf'
    generate_pdf(html_content, pdf_output_path)

    # Create the EmailMessage object without text_content
    subject = 'Your Email Subject'
    from_email = 'sanjay.singh@crebritech.com'
    to_email = 'srbc500@gmail.com'

    email_message = EmailMessage(
        subject,
        '',
        from_email,
        [to_email],
        headers={'Message-ID': 'foo'},
    )

    # Attach the PDF file
    with open(pdf_output_path, 'rb') as pdf_file:
        email_message.attach('output.pdf', pdf_file.read(), 'application/pdf')

    # Send the email
    email_message.send()

    # Delete the temporary PDF file
    os.remove(pdf_output_path)

    return HttpResponse('Email sent successfully')


def view_invoice(request, bill_id):
    header = PatientBillHistoryHead.objects.get(head_id=bill_id)
    details = PatientBillHistoryDetails.objects.filter(head_id=bill_id)
    context = {
        'bill_id': id,
        'header': header,
        'details': details,
    }
    print(context, '===============context')
    return render(request, 'email_template.html', context)


def mini_store_logout(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/')
def patient_billing_list(request):
    mini_medical_user_id = request.session.get('mini_medical_user_id')
    main_medical_user_id = request.session.get('main_medical_user_id')
    if mini_medical_user_id is not None:
        mini_medical_user_id = mini_medical_user_id
        mini_medical_details = Stores.objects.get(user_id=mini_medical_user_id)
        hospital_id = mini_medical_details.hospital.h_id

    elif main_medical_user_id is not None:
        main_medical_user_id = main_medical_user_id
        main_medical_details = Stores.objects.get(user_id=main_medical_user_id)
        hospital_id = main_medical_details.hospital.h_id

    patient_bill = HeaderPatient.objects.filter(appointment__hospital_id=hospital_id, bill_status='unbilled')
    context = {
        'patient_bill': patient_bill,
    }
    return render(request, 'patient_billing_list.html', context)


def generate_bill(request, head_id):
    mini_medical_user_id = request.session.get('mini_medical_user_id')
    main_medical_user_id = request.session.get('main_medical_user_id')

    if mini_medical_user_id is not None:
        mini_medical_user_id = mini_medical_user_id
        mini_medical_obj = Stores.objects.filter(user_id=mini_medical_user_id)
        if mini_medical_obj:
            store_id = mini_medical_obj[0].id
            hospital_id = mini_medical_obj[0].hospital.h_id
    elif main_medical_user_id is not None:
        main_medical_user_id = main_medical_user_id
        main_medical_obj = Stores.objects.filter(user_id=main_medical_user_id)
        if main_medical_obj:
            store_id = main_medical_obj[0].id
            hospital_id = main_medical_obj[0].hospital.h_id
    else:
        return redirect('/')
    loader = LookupField.objects.filter(title='loader')
    if loader:
        loader = loader[0].image.url
    else:
        loader = ''

    header = HeaderPatient.objects.get(head_id=head_id)
    details = DetailsPatient.objects.filter(header_id=head_id)
    context = {
        'head_id': head_id,
        'header': header,
        'details': details,
        'store_id': store_id,
        'hospital_id': hospital_id,
        'loader': loader,
    }
    return render(request, 'generate_bill1.html', context)


def generated_bill(request, id=0):
    if request.method == 'POST':
        mini_medical_user_id = request.session.get('mini_medical_user_id')
        main_medical_user_id = request.session.get('main_medical_user_id')
        if mini_medical_user_id is None and main_medical_user_id is None:
            return redirect('/')

        if mini_medical_user_id is not None:
            mini_medical_user_id = Stores.objects.get(user_id=mini_medical_user_id)
            mini_medical_store_id = mini_medical_user_id.id
        else:
            mini_medical_store_id = None

        if main_medical_user_id is not None:
            main_medical_user_id = Stores.objects.get(user_id=main_medical_user_id)
            main_medical_store_id = main_medical_user_id.id
        else:
            main_medical_store_id = None

        form = request.POST

        head_id = form.get('head_id')
        patient_id = form.get('patient_id')
        hospital_id = form.get('hospital_id')
        doctor_id = form.get('doctor_id')
        medicine_ids = form.getlist('medicine_id')
        qty = form.getlist('qty')
        price = form.getlist('price')
        total = form.getlist('total')
        cash_amount = form.get('cash_amount')
        online_amount = form.get('online_amount')
        remaining_amount = form.get('remaining_amount')
        g_amount = int(cash_amount) + int(online_amount) + int(remaining_amount)

        msg = 'something went wrong!'
        status = 0
        bill_id = 0
        loop_count = 0
        if id == 0:
            history = PatientBillHistoryHead.objects.create(header_patient_id=head_id,
                                                            patient_id=patient_id,
                                                            hospital_id=hospital_id,
                                                            doctor_id=doctor_id,
                                                            grand_total=g_amount,
                                                            cash=cash_amount,
                                                            online=online_amount,
                                                            remaining=remaining_amount,
                                                            mini_store_id=mini_medical_store_id,
                                                            main_store_id=main_medical_store_id,
                                                            )
            if history:
                for i in range(len(medicine_ids)):
                    if medicine_ids[i] and qty[i] != '0' and qty[i]:
                        PatientBillHistoryDetails.objects.create(head_id=history.head_id,
                                                                 medicine_id=medicine_ids[i],
                                                                 qty=qty[i],
                                                                 price=price[i],
                                                                 total=total[i],
                                                                 )
                        if mini_medical_user_id is not None:
                            medicine_qty = MiniStoreMedicine.objects.get(medicine_id=medicine_ids[i],
                                                                         to_store_id=mini_medical_user_id,
                                                                         hospital_id=hospital_id)
                            medi_qty = medicine_qty.qty
                            medicine_qty.qty = int(medi_qty) - int(qty[i])
                            medicine_qty.save()
                        else:
                            medicine_qty = MainStoreMedicine.objects.get(medicine_id=medicine_ids[i],
                                                                         to_main_store_id=main_medical_store_id,
                                                                         hospital_id=hospital_id)
                            medi_qty = medicine_qty.qty
                            medicine_qty.qty = int(medi_qty) - int(qty[i])
                            medicine_qty.save()

                        loop_count += 1
                if loop_count > 0:
                    header = HeaderPatient.objects.filter(head_id=head_id).update(bill_status='billed')
                    if header:
                        # this is function to send pdf
                        send_pdf_email(history.head_id)
                        # end this is function to send pdf
                        msg = 'Bill Generated Successfully '
                        status = 1
                        bill_id = history.head_id
                else:
                    PatientBillHistoryHead.objects.get(head_id=history.head_id).delete()
                    msg = 'Bill Generated Failed!'
            else:
                msg = 'Bill Generated Failed!'

        context = {
            'msg': msg,
            'status': status,
            'bill_id': bill_id,
        }
        return JsonResponse(context)

    else:
        header = PatientBillHistoryHead.objects.get(head_id=id)
        details = PatientBillHistoryDetails.objects.filter(head_id=id)
        context = {
            'bill_id': id,
            'header': header,
            'details': details,
        }
        return render(request, 'update_bill.html', context)


def new_customer_bill(request):
    mini_medical_user_id = request.session.get('mini_medical_user_id')
    main_medical_user_id = request.session.get('main_medical_user_id')
    if mini_medical_user_id is None and main_medical_user_id is None:
        return redirect('/')

    if mini_medical_user_id is not None:
        mini_medical_user_id = Stores.objects.get(user_id=mini_medical_user_id, store_type='MINI_MEDICAL_STORE')
        store_id = mini_medical_user_id.id
        hospital_id = mini_medical_user_id.hospital.h_id

    if main_medical_user_id is not None:
        main_medical_user_id = Stores.objects.get(user_id=main_medical_user_id, store_type='MAIN_MEDICAL_STORE')
        store_id = main_medical_user_id.id
        hospital_id = main_medical_user_id.hospital.h_id

    loader = LookupField.objects.filter(title='loader')
    if loader:
        loader = loader[0].image.url
    else:
        loader = ''

    context = {
        'hospital_id': hospital_id,
        'store_id': store_id,
        'loader': loader,
    }
    return render(request, 'new_customer_bill.html', context)


def new_customer_generate_bill(request, bill_id):
    if request.method == 'POST':
        mini_medical_user_id = request.session.get('mini_medical_user_id')
        main_medical_user_id = request.session.get('main_medical_user_id')
        hospital_id = None
        if mini_medical_user_id is None and main_medical_user_id is None:
            return redirect('/')

        if mini_medical_user_id is not None:
            mini_medical_user_id = Stores.objects.get(user_id=mini_medical_user_id)
            hospital_id = mini_medical_user_id.hospital.h_id
            mini_medical_store_id = mini_medical_user_id.id
        else:
            mini_medical_store_id = None

        if main_medical_user_id is not None:
            main_medical_user_id = Stores.objects.get(user_id=main_medical_user_id)
            hospital_id = main_medical_user_id.hospital.h_id
            main_medical_store_id = main_medical_user_id.id
        else:
            main_medical_store_id = None

        header_patient_id = None
        patient_id = None
        doctor_id = None
        form = request.POST

        medicine_ids = form.getlist('medicine_id')
        qty = form.getlist('qty')
        price = form.getlist('price')
        total = form.getlist('total')
        cash_amount = form.get('cash_amount')
        online_amount = form.get('online_amount')
        remaining_amount = form.get('remaining_amount')

        g_amount = int(cash_amount) + int(online_amount) + int(remaining_amount)

        msg = ''
        status = 0
        loop_count = 0
        if bill_id == 0:
            history = PatientBillHistoryHead.objects.create(header_patient_id=header_patient_id,
                                                            patient_id=patient_id,
                                                            hospital_id=hospital_id,
                                                            doctor_id=doctor_id,
                                                            grand_total=g_amount,
                                                            cash=cash_amount,
                                                            online=online_amount,
                                                            remaining=remaining_amount,
                                                            mini_store_id=mini_medical_store_id,
                                                            main_store_id=main_medical_store_id,
                                                            )
            if history:
                for i in range(len(medicine_ids)):
                    if medicine_ids[i] and qty[i] != '0' and qty[i]:
                        PatientBillHistoryDetails.objects.create(head_id=history.head_id,
                                                                 medicine_id=medicine_ids[i],
                                                                 qty=qty[i],
                                                                 price=price[i],
                                                                 total=total[i],
                                                                 )
                        if mini_medical_user_id is not None:
                            medicine_qty = MiniStoreMedicine.objects.get(medicine_id=medicine_ids[i],
                                                                         to_store_id=mini_medical_user_id,
                                                                         hospital_id=hospital_id)
                            print(medicine_qty, '=============medicine_qty')

                            medi_qty = medicine_qty.qty
                            print(medi_qty, '=============medi_qty')

                            print(qty[i], '=============qty[i]')
                            medicine_qty.qty = int(medi_qty) - int(qty[i])
                            medicine_qty.save()
                        else:
                            medicine_qty = MainStoreMedicine.objects.get(medicine_id=medicine_ids[i],
                                                                         to_main_store_id=main_medical_store_id,
                                                                         hospital_id=hospital_id)
                            medi_qty = medicine_qty.qty
                            medicine_qty.qty = int(medi_qty) - int(qty[i])
                            medicine_qty.save()

                        msg = 'Bill Generated Successfully '
                        status = 1
                if loop_count > 0:
                    send_pdf_email(history.head_id)
                else:
                    PatientBillHistoryHead.objects.get(head_id=history.head_id).delete()
                    msg = 'Bill Generated Failed!'
            else:
                msg = 'Bill Generated Failed!'
        else:
            pass

        context = {
            'msg': msg,
            'status': status,
            'bill_id': bill_id,
        }
        return JsonResponse(context)


def generated_billing_list(request):
    mini_medical_user_id = request.session.get('mini_medical_user_id')
    main_medical_user_id = request.session.get('main_medical_user_id')

    if mini_medical_user_id is None and main_medical_user_id is None:
        return redirect('/')

    if mini_medical_user_id is not None:
        mini_medical_user_id = Stores.objects.get(user_id=mini_medical_user_id)
        mini_medical_store_id = mini_medical_user_id.id
        generated_bill = PatientBillHistoryHead.objects.filter(mini_store_id=mini_medical_store_id).order_by('-head_id')

    if main_medical_user_id is not None:
        main_medical_user_id = Stores.objects.get(user_id=main_medical_user_id)
        main_medical_store_id = main_medical_user_id.id
        generated_bill = PatientBillHistoryHead.objects.filter(main_store_id=main_medical_store_id).order_by('-head_id')

    context = {
        'bill': generated_bill,
    }
    return render(request, 'generated_billing_list.html', context)
