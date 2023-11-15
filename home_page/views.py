from django.shortcuts import render

# Create your views here.
from site_settings.models import LookupField


def home_page(request):
    multi_login_back_img = LookupField.objects.filter(code='multi_login')
    if multi_login_back_img:
        multi_login_back_img = multi_login_back_img[0].image.url
    context = {
        'back_img': multi_login_back_img,
    }
    return render(request, 'multi_user_login.html', context)
