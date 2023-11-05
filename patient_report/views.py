from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from .models import HeaderPatient, DetailsPatient


def patient_history_report(request, appoint_id):
    head = HeaderPatient.objects.filter(appointment_id=appoint_id)
    medicine_history_date = ''
    if head:
        medicine_history_date = DetailsPatient.objects.filter(header_id=head[0].head_id).values_list('created_date',
                                                                                                     flat=True).distinct()[:10]
        if medicine_history_date:
            medicine_history_date = medicine_history_date

        status = 1
    else:
        head = ''

        status = 0
    context = {
        'status': status,
        'appoint_id': appoint_id,
        'head': head[0],
        'history_dates': medicine_history_date,
    }
    return render(request, 'patient_history_report.html', context)


def get_history(request):
    if request.method == 'GET':
        form = request.GET
        head_id = form.get('head_id')
        select_date = form.get('selectedDate')
        parsed_date = datetime.strptime(select_date, '%d-%m-%Y')
        formatted_date = parsed_date.strftime('%Y-%m-%d')
        details_medicine = DetailsPatient.objects.filter(header_id=head_id, created_date=formatted_date)
        data_list = []
        for i in details_medicine:
            data_dict = {}
            data_dict['detail_id'] = i.detail_id
            data_dict['medicine'] = i.medicine_details.name
            data_dict['dosage'] = i.dosage
            data_dict['frequency'] = i.frequency
            data_list.append(data_dict)
        context = {
            'data_list': data_list,
        }
        return JsonResponse(context)
