from django.shortcuts import render, redirect


# Create your views here.
from accounts.models import HospitalUser


def dashboard(request):
    hospital_user_id = request.session.get('hospital_user_id')
    print(hospital_user_id, '==========hospital_user_id')
    if hospital_user_id == None:
        return redirect('/accounts/hospital-login/')
    else:
        h_data = HospitalUser.objects.get(user_id=hospital_user_id)
    context = {
        'hospital_name': h_data.user.full_name
    }
    return render(request, 'hospital_dashboard.html', context)
