from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from accounts.models import Stores
from store.models import Medicine, MainStoreMedicine, MedicineTransferHistory, MiniStoreMedicine


def medicine_transaction(medicine_id, qty, from_store_id, to_store_id, hospital_id):
    MedicineTransferHistory.objects.create(medicine_id=medicine_id,
                                           qty=qty,
                                           from_store_id=from_store_id,
                                           to_store_id=to_store_id,
                                           hospital_id=hospital_id,
                                           )


def add_medicine(request, main_store_id):
    store = Stores.objects.get(id=main_store_id, store_type='MAIN_MEDICAL_STORE')
    hospital_id = store.hospital.h_id
    if request.method == 'POST':
        form = request.POST
        batch_no = form.get('batch_no')
        batch_no = batch_no.upper()
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
                                           manufacturer=manufacturer,
                                           expiration=expiration,
                                           main_store_id=main_store_id,
                                           hospital_id=hospital_id
                                           )
        if medicine:
            medicine_id = medicine.medicine_id
            MainStoreMedicine.objects.create(medicine_id=medicine_id,
                                             qty=quantity,
                                             from_mini_store_id=None,
                                             to_main_store_id=main_store_id,
                                             hospital_id=hospital_id,
                                             )
            to_store_id = main_store_id
            from_store_id = main_store_id
            medicine_transaction(medicine_id, quantity, from_store_id, to_store_id, hospital_id)

            return redirect(f'/store/add_medicine/{main_store_id}/')
    else:
        return render(request, 'add_medicine.html')


def search_medicine(request):
    if request.method == 'GET':
        form = request.GET
        hospital_id = form.get('hospital_id')
        search_value = form.get('search_value')
        hospi_query = Q(hospital__h_id=hospital_id)
        medicine = Medicine.objects.filter(hospi_query, Q(name__icontains=search_value) |
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


def main_medical_store_dashboard(request):
    main_medical_user_id = request.session.get('main_medical_user_id')
    if main_medical_user_id is None:
        return redirect('/accounts/main_medical_store_login/')
    else:
        main_medical_store = Stores.objects.get(user_id=main_medical_user_id)
        hospital_id = main_medical_store.hospital.h_id
        main_store_id = main_medical_store.id
        medicine = MainStoreMedicine.objects.filter(to_main_store_id=main_store_id)

        mini_stores = Stores.objects.filter(hospital_id=hospital_id, store_type='MINI_MEDICAL_STORE')
        context = {
            'main_store_id': main_store_id,
            'main_medical_store': main_medical_store,
            'medicine': medicine,
            'mini_stores': mini_stores,
            'hospital_id': hospital_id
        }
        return render(request, 'main_medical_store_dashboard.html', context)


def mini_medical_store_dashboard(request):
    mini_medical_user_id = request.session.get('mini_medical_user_id')
    if mini_medical_user_id is None:
        return redirect('/accounts/mini_medical_store_login/')
    else:
        mini_medical_store = Stores.objects.get(user_id=mini_medical_user_id, store_type='MINI_MEDICAL_STORE')
        mini_medical_store_id = mini_medical_store.id
        hospital_id = mini_medical_store.hospital.h_id
        medicine = MiniStoreMedicine.objects.filter(to_store_id=mini_medical_store_id)
        context = {
            'hospital_id': hospital_id,
            'mini_medical_store_id': mini_medical_store_id,
            'mini_medical_store': mini_medical_store,
            'medicine': medicine,
        }
        return render(request, 'mini_medical_store_dashboard.html', context)


def get_mini_store_model_data(request):
    if request.method == 'GET':
        form = request.GET
        main_store_id = form.get('main_store_id')
        mini_store_id = form.get('mini_medical_store_id')
        hospital_id = form.get('hospital_id')

        mini_store_list = []
        if main_store_id:
            mini_store = Stores.objects.filter(hospital_id=hospital_id, store_type='MINI_MEDICAL_STORE')
            if mini_store:
                for i in mini_store:
                    data_dict = {}
                    data_dict['mini_store_id'] = i.id
                    data_dict['mini_store_name'] = i.user.full_name
                    mini_store_list.append(data_dict)

        else:
            if mini_store_id:
                mini_store = Stores.objects.filter(hospital_id=hospital_id, store_type='MINI_MEDICAL_STORE').exclude(
                    id=mini_store_id)
                if mini_store:
                    for i in mini_store:
                        data_dict = {}
                        data_dict['mini_store_id'] = i.id
                        data_dict['mini_store_name'] = i.user.full_name
                        mini_store_list.append(data_dict)
        context = {
            'mini_store': mini_store_list,
        }
        return JsonResponse(context)


def transfer_medicine_from_main_to_mini(request):
    if request.method == 'GET':
        form = request.GET
        hospital_id = form.get('hospital_id')
        from_store = form.get('main_store_id')
        medicine = form.get('medicine_id')
        to_store = form.get('mini_store_id')
        medicine_qty = form.get('medicine_qty')

        is_medicine = MiniStoreMedicine.objects.filter(medicine_id=medicine,
                                                       to_store_id=to_store,
                                                       hospital_id=hospital_id,
                                                       ).exists()

        if is_medicine == False:
            mini_store_obj = MiniStoreMedicine.objects.create(medicine_id=medicine,
                                                              qty=medicine_qty,
                                                              from_store_id=from_store,
                                                              to_store_id=to_store,
                                                              hospital_id=hospital_id,
                                                              )
            if mini_store_obj:
                main_medicine_qty = MainStoreMedicine.objects.get(to_main_store_id=from_store, medicine_id=medicine)
                main_medicine_qty = main_medicine_qty.qty
                qty = int(main_medicine_qty) - int(medicine_qty)
                main_store_obj = MainStoreMedicine.objects.filter(to_main_store_id=from_store,
                                                                  medicine_id=medicine).update(
                    qty=qty)
                if main_store_obj:
                    medicine_transaction(medicine, medicine_qty, from_store, to_store, hospital_id)
                msg = 'Medicine transfer successful.'
                status = 1
        else:
            mini_store_obj = MiniStoreMedicine.objects.get(medicine_id=medicine,
                                                           from_store_id=from_store,
                                                           to_store_id=to_store,
                                                           hospital_id=hospital_id,
                                                           )
            update_qty = int(mini_store_obj.qty) + int(medicine_qty)

            mini_store_obj = MiniStoreMedicine.objects.filter(medicine_id=medicine,
                                                              from_store_id=from_store,
                                                              to_store_id=to_store,
                                                              hospital_id=hospital_id,
                                                              ).update(qty=update_qty, )
            if mini_store_obj:
                main_medicine_qty = MainStoreMedicine.objects.get(to_main_store_id=from_store, medicine_id=medicine)
                main_medicine_qty = main_medicine_qty.qty
                qty = int(main_medicine_qty) - int(medicine_qty)
                main_store_obj = MainStoreMedicine.objects.filter(to_main_store_id=from_store,
                                                                  medicine_id=medicine).update(
                    qty=qty)
                if main_store_obj:
                    medicine_transaction(medicine, medicine_qty, from_store, to_store, hospital_id)

                msg = 'Medicine transfer successful.'
                status = 1

        context = {
            'msg': msg,
            'status': status
        }
        return JsonResponse(context)


def transfer_medicine_mini_to_mini_store(request):
    if request.method == 'GET':
        form = request.GET
        hospital_id = form.get('hospital_id')
        from_store_id = form.get('from_mini_medical_store_id')
        to_store_id = form.get('to_mini_store_id')
        medicine_id = form.get('medicine_id')
        medicine_qty = form.get('medicine_qty')
        status = 0
        msg = 'Medicine not Transferred .'

        is_medicine = MiniStoreMedicine.objects.filter(medicine_id=medicine_id,
                                                       to_store_id=to_store_id,
                                                       hospital_id=hospital_id,
                                                       ).exists()
        if is_medicine == False:
            mini_store_obj = MiniStoreMedicine.objects.create(medicine_id=medicine_id,
                                                              qty=medicine_qty,
                                                              from_store_id=from_store_id,
                                                              to_store_id=to_store_id,
                                                              hospital_id=hospital_id,
                                                              )
            if mini_store_obj:
                main_medicine_qty = MiniStoreMedicine.objects.get(to_store_id=from_store_id,
                                                                  medicine_id=medicine_id)
                main_medicine_qty = main_medicine_qty.qty
                qty = int(main_medicine_qty) - int(medicine_qty)
                main_store_obj = MiniStoreMedicine.objects.filter(to_store_id=from_store_id,
                                                                  medicine_id=medicine_id).update(qty=qty)
                if main_store_obj:
                    medicine_transaction(medicine_id, medicine_qty, from_store_id, to_store_id, hospital_id)
                msg = 'Medicine transfer successful.'
                status = 1
        else:
            mini_store_obj = MiniStoreMedicine.objects.get(medicine_id=medicine_id,
                                                           to_store_id=to_store_id,
                                                           hospital_id=hospital_id,
                                                           )
            if mini_store_obj:
                mini_medicine_qty = mini_store_obj.qty
                qty = int(mini_medicine_qty) + int(medicine_qty)
                mini_store_obj = MiniStoreMedicine.objects.filter(medicine_id=medicine_id,
                                                                  to_store_id=to_store_id,
                                                                  hospital_id=hospital_id, ).update(qty=qty)
                if mini_store_obj:
                    # update mini store records
                    mini_store_records = MiniStoreMedicine.objects.get(medicine_id=medicine_id,
                                                                       to_store_id=from_store_id,
                                                                       hospital_id=hospital_id)

                    qty = int(mini_store_records.qty) - int(medicine_qty)
                    mini_store_obj = MiniStoreMedicine.objects.filter(medicine_id=medicine_id,
                                                                      to_store_id=from_store_id,
                                                                      hospital_id=hospital_id).update(qty=qty)
                    # end update mini store records
                    if mini_store_obj:
                        medicine_transaction(medicine_id, medicine_qty, from_store_id, to_store_id, hospital_id)
                    msg = 'Medicine transfer successful.'
                    status = 1

        context = {
            'msg': msg,
            'status': status
        }
        return JsonResponse(context)


def check_medicine_qty(request):
    if request.method == 'GET':
        form = request.GET
        store_id = form.get('store_id')
        hospital_id = form.get('hospital_id')
        store = MainStoreMedicine.objects.filter(to_main_store_id=store_id, hospital_id=hospital_id)
        if store:
            store_qty = store[0].qty
        else:
            store = MiniStoreMedicine.objects.filter(to_store_id=store_id, hospital_id=hospital_id)
            store_qty = store[0].qty
        context = {
            'store_id': store_id,
            'hospital_id': hospital_id,
            'store_qty': store_qty,

        }
        return JsonResponse(context)


def view_mini_stores_record(request, mini_store_id, hospital_id):
    if request.method == 'GET':
        medicine = MiniStoreMedicine.objects.filter(to_store_id=mini_store_id)
        mini_store = Stores.objects.filter(hospital_id=hospital_id, store_type='MINI_MEDICAL_STORE')

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
