from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.models import HospitalUser
from .models import Medicine, MappingMedicine, MainStore, MainMedicalStoreMedicineTransactionHistory, MiniStore, \
    MappingMiniStorMedicine


# Create your views here.
def add_medicine(request):
    if request.method == 'POST':
        hospital_user_id = request.session.get('hospital_user_id')
        h_id = HospitalUser.objects.get(user_id=hospital_user_id)
        form = request.POST
        medicine_name = form.get('medicineName')
        description = form.get('description')
        price = form.get('price')
        expiration = form.get('expiration_date')
        manufacturer = form.get('manufacturer')
        medicine = Medicine.objects.create(name=medicine_name,
                                           description=description,
                                           price=price,
                                           manufacturer=manufacturer,
                                           expiration=expiration,
                                           hospital_id=h_id.h_id,
                                           )
        if medicine:
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


def transfer_search_medicine(request):
    if request.method == 'GET':
        hospital_user_id = request.session.get('hospital_user_id')
        h_id = HospitalUser.objects.get(user_id=hospital_user_id)
        form = request.GET
        search_value = form.get('search_value')
        medicine = Medicine.objects.filter(name__icontains=search_value, hospital_id=h_id.h_id)
        data_list = []
        for i in medicine:
            data_dict = {}
            data_dict['id'] = i.medicine_id
            data_dict['name'] = i.name.capitalize()
            data_dict['description'] = i.description
            data_list.append(data_dict)

        context = {
            'results': data_list,
        }
        return JsonResponse(context)


def mapping_medicine(request):
    if request.method == 'POST':
        hospital_user_id = request.session.get('hospital_user_id')
        h_id = HospitalUser.objects.get(user_id=hospital_user_id)
        main_store = MainStore.objects.get(hospital_id=h_id.h_id)
        main_store_id = main_store.main_store_id
        form = request.POST
        medicine_ids = form.getlist('medicine_id')
        qty = form.getlist('qty')
        for i in range(len(medicine_ids)):
            if medicine_ids[i] != '' and qty[i]:
                obj = MappingMedicine.objects.create(medicine_id=medicine_ids[i],
                                                     main_qty=qty[i],
                                                     main_store_user_id=main_store_id,
                                                     )
                if obj:
                    main_medicine_transaction(obj.mapping_id, qty[i])
            else:
                print(medicine_ids[i], '===============medicine_ids[i]')
                print(qty[i], '===============qty[i]')
        return redirect('/store/mapping-medicine/')
    else:
        hospital_user_id = request.session.get('hospital_user_id')
        h_id = HospitalUser.objects.get(user_id=hospital_user_id)
        main_store = MainStore.objects.filter(hospital_id=h_id.h_id)
        if main_store:
            main_store_id = main_store[0].main_store_id
        else:
            return redirect('/accounts/main_medical_store_registration/')
        context = {
            'main_store_id': main_store_id
        }
        return render(request, 'transfer_medicine_to_main.html', context)


def main_medicine_transaction(mapping_id, qty):
    MainMedicalStoreMedicineTransactionHistory.objects.create(mapping_medicine_id=mapping_id,
                                                              trans_qty=qty,
                                                              )


def view_main_store(request, main_store_id):
    if request.method == 'GET':
        medicine = MappingMedicine.objects.filter(main_store_user_id=main_store_id)
        hospital_id = medicine[0].main_store_user.hospital.h_id
        mini_store = MiniStore.objects.all()
        if medicine:
            context = {
                'hospital_id': hospital_id,
                'main_store_id': main_store_id,
                'medicine': medicine,
                'mini_store': mini_store,
            }
            return render(request, 'view_main_store.html', context)
        else:
            return redirect('/store/mapping-medicine/')

def view_mini_stores_record(request, mini_store_id, hospital_id):
    if request.method == 'GET':
        medicine = MappingMiniStorMedicine.objects.filter(mini_store_user_id=mini_store_id)
        mini_store = MiniStore.objects.filter(hospital_id=hospital_id)
        if medicine:
            context = {
                'hospital_id': hospital_id,
                'mini_store_id': mini_store_id,
                'mini_store': mini_store,
                'medicine': medicine,
            }
            return render(request, 'mini_store_record.html', context)
        else:
            context = {
                'hospital_id': hospital_id,
                'mini_store_id': mini_store_id,
                'mini_store': mini_store,
                'medicine': medicine,
            }
            return render(request, 'mini_store_record.html', context)


def get_mini_store_model_data(request):
    if request.method == 'GET':
        form = request.GET
        main_store_id = form.get('main_store_id')
        print(main_store_id, '=======main_store_id')
        main_store = MainStore.objects.filter(main_store_id=main_store_id)
        print(main_store, '==============main_store')
        mini_store_list = []
        if main_store:
            hospital_id = main_store[0].hospital_id
            print(hospital_id, '=======hospital_id')
            if hospital_id:
                mini_store = MiniStore.objects.filter(hospital_id=hospital_id)
                if mini_store:
                    for i in mini_store:
                        data_dict = {}
                        data_dict['mini_store_id'] = i.mini_store_id
                        data_dict['mini_store_name'] = i.mini_store_user.full_name
                        mini_store_list.append(data_dict)

        context = {
            'mini_store': mini_store_list,
        }
        return JsonResponse(context)


def transfer_medicine_to_mini_store(request):
    if request.method == 'GET':
        form = request.GET
        main_store_id = form.get('main_store_id')
        mini_store_id = form.get('mini_store_id')
        medicine_id = form.get('medicine_id')
        medicine_qty = form.get('medicine_qty')
        status = 0
        msg = 'Medicine not Transferred .'
        is_exists = MappingMiniStorMedicine.objects.filter(medicine_id=medicine_id,
                                                           mini_store_user_id=mini_store_id).exists()
        if is_exists == True:
            obj = MappingMiniStorMedicine.objects.get(medicine_id=medicine_id, mini_store_user_id=mini_store_id)
            obj_mini_qty = obj.mini_qty
            obj_mini_qty = int(obj_mini_qty) + int(medicine_qty)

            obj = MappingMiniStorMedicine.objects.filter(medicine_id=medicine_id,
                                                         mini_store_user_id=mini_store_id).update(mini_qty=obj_mini_qty)
        else:
            obj = MappingMiniStorMedicine.objects.create(mini_qty=medicine_qty,
                                                         medicine_id=medicine_id,
                                                         mini_store_user_id=mini_store_id
                                                         )
        if obj:
            medicine = MappingMedicine.objects.filter(mapping_id=medicine_id, main_store_user_id=main_store_id)
            if medicine:
                medicine = medicine[0].main_qty
            obj = MappingMedicine.objects.filter(mapping_id=medicine_id, main_store_user_id=main_store_id).update(
                main_qty=int(medicine) - int(medicine_qty))
            if obj:
                status = 1
                msg = 'medicine transfer to mini store successfully.'
            else:
                status = status
            context = {
                'status': status,
                'msg': msg
            }
            return JsonResponse(context)
