from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Medicine, MappingMedicine


# Create your views here.
def add_medicine(request):
    if request.method == 'POST':
        form = request.POST
        medicine_name = form.get('medicineName')
        description = form.get('description')
        Medicine.objects.create(name=medicine_name,
                                description=description)

        return redirect('/store/add_medicine/')

    else:
        return render(request, 'add_medicine.html')


def search_medicine(request):
    if request.method == 'GET':
        form = request.GET
        search_value = form.get('search_value')
        medicine = MappingMedicine.objects.filter(medicine__name__icontains=search_value)
        data_list = []
        for i in medicine:
            data_dict = {}
            data_dict['id'] = i.mapping_id
            data_dict['name'] = i.medicine.name.capitalize()
            data_list.append(data_dict)

        context = {
            'results': data_list,
        }
        return JsonResponse(context)
