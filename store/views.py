from django.shortcuts import render, redirect
from .models import Medicine


# Create your views here.
def add_medicine(request):
    if request.method == 'POST':
        form = request.POST
        medicine_name = form.get('medicineName')
        description = form.get('description')
        price = form.get('price')
        quantity = form.get('quantity')
        manufacturer = form.get('manufacturer')
        expiration_date = form.get('expiration_date')
        main_store = 1

        Medicine.objects.create(name=medicine_name,
                                description=description,
                                manufacturer=manufacturer,
                                price=price,
                                quantity=quantity,
                                expiration_date=expiration_date,
                                main_store_id=main_store)

        return redirect('/store/add_medicine/')

    else:
        return render(request, 'add_medicine.html')
