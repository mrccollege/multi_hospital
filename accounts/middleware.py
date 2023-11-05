from django.http import HttpResponseRedirect


class AuthRequiredMiddleware(object):
    print('user_is active')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self, request):
        if request.user.is_authenticated:
            next = request.GET.get('next')
            print('user_is active')
            return HttpResponseRedirect('/')  # or http response
        return None
