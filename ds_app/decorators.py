from django.contrib import messages
from django.shortcuts import redirect

def check_authentication(func):
    def inner_func(request, *args, **kwargs):
        print("check_authentication is called!")
        print("request data from decorator:", request.POST)
        if not request.user.is_authenticated:
            messages.success(request, f"Please login to proceed further!")
            return redirect('login')
        return func(request, *args, **kwargs)
    return inner_func


def check_superadmin_authentication(func):
    print("check_superadmin_authentication is called!")
    def inner_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return func(request, *args, **kwargs)
        messages.error(request, f"Only admin can send the mail..!")
        # return redirect('')
    return inner_func