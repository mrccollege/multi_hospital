from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.models import HospitalUser
from .models import Medicine, MainStore, MainMedicalStoreMedicineTransactionHistory, MiniStore, \
    MappingMiniStorMedicine


# Create your views here.
def add_medicine(request, main_store_id):
    if request.method == 'POST':
        form = request.POST
        batch_no = form.get('batch_no')
        medicine_name = form.get('medicineName')
        description = form.get('description')
        price = form.get('price')
        quantity = form.get('quantity')
        expiration = form.get('expiration_date')
        manufacturer = form.get('manufacturer')
        manufacturer = manufacturer.title()
        medicine = Medicine.objects.create(name=medicine_name,
                                           batch_no=batch_no,
                                           description=description,
                                           price=price,
                                           qty=quantity,
                                           manufacturer=manufacturer,
                                           expiration=expiration,
                                           main_store_id=main_store_id,
                                           )
        if medicine:
            return redirect(f'/store/add_medicine/{main_store_id}/')
    else:
        return render(request, 'add_medicine.html')


def search_medicine(request):
    if request.method == 'GET':
        form = request.GET
        search_value = form.get('search_value')
        medicine = Medicine.objects.filter(Q(name__icontains=search_value) |
                                           Q(batch_no__icontains=search_value))
        data_list = []
        for i in medicine:
            data_dict = {}
            data_dict['id'] = i.medicine_id
            data_dict['name'] = i.name.capitalize()
            data_dict['batch_no'] = i.batch_no if i.batch_no else ''
            data_dict['price'] = i.price
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
                obj = Medicine.objects.create(medicine_id=medicine_ids[i],
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


def main_medical_store_dashboard(request):
    main_medical_user_id = request.session.get('main_medical_user_id')
    if main_medical_user_id is None:
        return redirect('/accounts/main_medical_store_login/')
    else:
        main_medical_store = MainStore.objects.get(main_store_user_id=main_medical_user_id)
        main_medical_store_id = main_medical_store.main_store_id
        medicine = Medicine.objects.filter(main_store_id=main_medical_store_id)

        mini_stores = MiniStore.objects.filter(hospital_id=main_medical_store.hospital_id)
        context = {
            'main_store_id': main_medical_store_id,
            'main_medical_store': main_medical_store,
            'medicine': medicine,
            'mini_stores': mini_stores,
            'hospital_id': main_medical_store.hospital_id
        }
        return render(request, 'main_medical_store_dashboard.html', context)


def mini_medical_store_dashboard(request):
    mini_medical_user_id = request.session.get('mini_medical_user_id')
    if mini_medical_user_id is None:
        return redirect('/accounts/mini_medical_store_login/')
    else:
        mini_medical_store = MiniStore.objects.get(mini_store_user_id=mini_medical_user_id)
        mini_medical_store_id = mini_medical_store.mini_store_id
        medicine = MappingMiniStorMedicine.objects.filter(mini_store_user_id=mini_medical_store_id)
        print(medicine, '==========medicine')
        context = {
            'mini_medical_store_id': mini_medical_store_id,
            'mini_medical_store': mini_medical_store,
            'medicine': medicine,
        }
        return render(request, 'mini_medical_store_dashboard.html', context)


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
            medicine = Medicine.objects.filter(medicine_id=medicine_id, main_store_id=main_store_id)
            if medicine:
                medicine = medicine[0].qty
            obj = Medicine.objects.filter(medicine_id=medicine_id, main_store_id=main_store_id).update(qty=int(medicine) - int(medicine_qty))
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
