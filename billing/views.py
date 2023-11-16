from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from billing.models import PatientBillHistory, PatientBillHistoryHead, PatientBillHistoryDetails
from patient_report.models import HeaderPatient, DetailsPatient
from store.models import MiniStore, MappingMiniStorMedicine
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa


def mini_store_logout(request):
    logout(request)
    return redirect('/accounts/mini_medical_store_login/')


@login_required(login_url='/accounts/mini_medical_store_login/')
def patient_billing_list(request):
    mini_medical_user_id = request.session['mini_medical_user_id']
    mini_medical_details = MiniStore.objects.get(mini_store_user_id=mini_medical_user_id)
    hospital_id = mini_medical_details.hospital_id
    patient_bill = HeaderPatient.objects.filter(appointment__hospital_id=hospital_id, bill_status='unbilled')
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
        mini_medical_user_id = request.session.get('mini_medical_user_id')
        if mini_medical_user_id is None:
            return redirect('/accounts/mini_medical_store_login/')
        mini_medical_user_id = MiniStore.objects.get(mini_store_user_id=mini_medical_user_id)
        mini_medical_user_id = mini_medical_user_id.mini_store_id
        if mini_medical_user_id is None:
            return redirect('/accounts/mini_medical_store_login/')

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

        msg = ''
        status = 0
        bill_id = 0
        if id == 0:
            history = PatientBillHistoryHead.objects.create(header_patient_id=head_id,
                                                            patient_id=patient_id,
                                                            hospital_id=hospital_id,
                                                            doctor_id=doctor_id,
                                                            grand_total=g_amount,
                                                            cash=cash_amount,
                                                            online=online_amount,
                                                            remaining=remaining_amount,
                                                            mini_store_id=mini_medical_user_id,
                                                            )
            if history:
                for i in range(len(medicine_ids)):
                    if medicine_ids[i]:
                        PatientBillHistoryDetails.objects.create(head_id=history.head_id,
                                                                 medicine_id=medicine_ids[i],
                                                                 qty=qty[i],
                                                                 price=price[i],
                                                                 total=total[i],
                                                                 )

                        medicine_qty = MappingMiniStorMedicine.objects.get(medicine_id=medicine_ids[i],
                                                                           mini_store_user_id=mini_medical_user_id)
                        medi_qty = medicine_qty.mini_qty
                        medicine_qty.mini_qty = int(medi_qty) - int(qty[i])
                        medicine_qty.save()

                header = HeaderPatient.objects.filter(head_id=head_id).update(bill_status='billed')
                if header:
                    msg = 'Bill Generated Successfully '
                    status = 1
                    bill_id = history.head_id
            else:
                msg = 'Bill Generated Failed!'

        else:
            history = PatientBillHistoryHead.objects.filter(head_id=id).update(grand_total=g_amount,
                                                                               cash=cash_amount,
                                                                               online=online_amount,
                                                                               remaining=remaining_amount,
                                                                               )
            if history:
                medi_details = PatientBillHistoryDetails.objects.filter(head_id=id)
                for j in medi_details:
                    medicine_qty = MappingMiniStorMedicine.objects.get(medicine_id=j.medicine.medicine_id,
                                                                       mini_store_user_id=mini_medical_user_id)
                    medi_qty = medicine_qty.mini_qty
                    medicine_qty.mini_qty = int(medi_qty) + int(j.qty)
                    medicine_qty.save()

                PatientBillHistoryDetails.objects.filter(head_id=id).delete()

                for i in range(len(medicine_ids)):
                    if medicine_ids[i]:
                        PatientBillHistoryDetails.objects.create(head_id=id,
                                                                 medicine_id=medicine_ids[i],
                                                                 qty=qty[i],
                                                                 price=price[i],
                                                                 total=total[i],
                                                                 )

                        medicine_qty = MappingMiniStorMedicine.objects.get(medicine_id=medicine_ids[i],
                                                                           mini_store_user_id=mini_medical_user_id)
                        medi_qty = medicine_qty.mini_qty
                        medicine_qty.mini_qty = int(medi_qty) - int(qty[i])
                        medicine_qty.save()
                header = HeaderPatient.objects.filter(head_id=head_id).update(bill_status='billed')
                if header:
                    msg = 'Bill Updated Successfully'
                    status = 1
                    bill_id = id
            else:
                msg = 'Bill Updated Failed!'

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
    if mini_medical_user_id is None:
        return redirect('/accounts/mini_medical_store_login/')
    else:
        return render(request, 'new_customer_bill.html')


def new_customer_generate_bill(request, bill_id):
    if request.method == 'POST':
        mini_medical_user_id = request.session.get('mini_medical_user_id')
        if mini_medical_user_id is None:
            return redirect('/accounts/mini_medical_store_login/')
        mini_medical_user_id = MiniStore.objects.get(mini_store_user_id=mini_medical_user_id)
        hospital_id = mini_medical_user_id.hospital.h_id
        mini_medical_user_id = mini_medical_user_id.mini_store_id

        if mini_medical_user_id is None:
            return redirect('/accounts/mini_medical_store_login/')

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
        if bill_id == 0:
            history = PatientBillHistoryHead.objects.create(header_patient_id=None,
                                                            hospital_id=hospital_id,
                                                            patient_id=None,
                                                            doctor_id=None,
                                                            grand_total=g_amount,
                                                            cash=cash_amount,
                                                            online=online_amount,
                                                            remaining=remaining_amount,
                                                            mini_store_id=mini_medical_user_id,
                                                            )
            if history:
                for i in range(len(medicine_ids)):
                    if medicine_ids[i]:
                        PatientBillHistoryDetails.objects.create(head_id=history.head_id,
                                                                 medicine_id=medicine_ids[i],
                                                                 qty=qty[i],
                                                                 price=price[i],
                                                                 total=total[i],
                                                                 )

                        medicine_qty = MappingMiniStorMedicine.objects.get(medicine_id=medicine_ids[i],
                                                                           mini_store_user_id=mini_medical_user_id)
                        medi_qty = medicine_qty.mini_qty
                        medicine_qty.mini_qty = int(medi_qty) - int(qty[i])
                        medicine_qty.save()

                msg = 'Bill Generated Successfully '
                status = 1
                bill_id = history.head_id

            else:
                msg = 'Bill Generated Failed!'

        else:
            history = PatientBillHistoryHead.objects.filter(head_id=bill_id).update(grand_total=g_amount,
                                                                                    cash=cash_amount,
                                                                                    online=online_amount,
                                                                                    remaining=remaining_amount,
                                                                                    )
            if history:
                medi_details = PatientBillHistoryDetails.objects.filter(head_id=bill_id)
                for j in medi_details:
                    medicine_qty = MappingMiniStorMedicine.objects.get(medicine_id=j.medicine.medicine_id,
                                                                       mini_store_user_id=mini_medical_user_id)
                    medi_qty = medicine_qty.mini_qty
                    medicine_qty.mini_qty = int(medi_qty) + int(j.qty)
                    medicine_qty.save()

                PatientBillHistoryDetails.objects.filter(head_id=bill_id).delete()

                for i in range(len(medicine_ids)):
                    if medicine_ids[i]:
                        PatientBillHistoryDetails.objects.create(head_id=bill_id,
                                                                 medicine_id=medicine_ids[i],
                                                                 qty=qty[i],
                                                                 price=price[i],
                                                                 total=total[i],
                                                                 )

                        medicine_qty = MappingMiniStorMedicine.objects.get(medicine_id=medicine_ids[i],
                                                                           mini_store_user_id=mini_medical_user_id)
                        medi_qty = medicine_qty.mini_qty
                        medicine_qty.mini_qty = int(medi_qty) - int(qty[i])
                        medicine_qty.save()

                msg = 'Bill Updated Successfully'
                status = 1
                bill_id = bill_id
            else:
                msg = 'Bill Updated Failed!'

        context = {
            'msg': msg,
            'status': status,
            'bill_id': bill_id,
        }
        return JsonResponse(context)


def generated_billing_list(request):
    mini_medical_user_id = request.session.get('mini_medical_user_id')
    if mini_medical_user_id is None:
        return redirect('/accounts/mini_medical_store_login/')
    mini_medical_user_id = MiniStore.objects.get(mini_store_user_id=mini_medical_user_id)
    mini_medical_user_id = mini_medical_user_id.mini_store_id
    if mini_medical_user_id is None:
        return redirect('/accounts/mini_medical_store_login/')

    generated_bill = PatientBillHistoryHead.objects.filter(mini_store_id=mini_medical_user_id).order_by('-head_id')

    context = {
        'bill': generated_bill,
    }
    return render(request, 'generated_billing_list.html', context)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def generate_pdf(request, bill_id):
    if bill_id is not None:
        invoice = PatientBillHistory.objects.get(id=bill_id)
        medicine = list(invoice.medicine)
        qty = invoice.qty
        price = invoice.price
        medicine_list = []

        for i in range(len(list(medicine))):
            medi = MappingMiniStorMedicine.objects.get(medicine_id=medicine[i])
            medi_dict = {}
            medi_dict['medicine_name'] = medi.medicine.name
            medi_dict['medicine_qty'] = qty[i]
            medi_dict['medicine_price'] = price[i]

            medicine_list.append(medi_dict)

        context = {
            'bill_id': bill_id,
            'data_list': medicine_list,
        }
    pdf = render_to_pdf('render_pdf.html', context)

    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "your_Bill.pdf"  # Change the filename accordingly
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    return HttpResponse("Error generating PDF")


def send_email(request, bill_id):
    invoice_detail = PatientBillHistory.objects.get(id=bill_id)
    patient = invoice_detail.header_patient.appointment.patient.user.full_name
    recipient_list = invoice_detail.header_patient.appointment.patient.user.email
    message = f"HELLO, {patient}"
    subject = 'Your Bill Generated'
    from_email = 'info@sanjay.solutions'
    # Generate the PDF using the PDF view
    pdf_response = generate_pdf(request, bill_id)
    if pdf_response:
        pdf_content = pdf_response.content

        # Create an EmailMessage instance
        email = EmailMessage(subject, message, from_email, [recipient_list])
        email.attach("your_pdf_filename.pdf", pdf_content, 'application/pdf')  # Attach the PDF

        try:
            email.send()
            # send_pd_whatsapp(pary_contact, subject, recipient_list)
            # send_whatsapp_message('hello geeta')
            return HttpResponse("Email sent successfully")
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}")
    else:
        return HttpResponse("Error generating PDF")
