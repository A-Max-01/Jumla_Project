from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return view_func(request, *args, **kwargs)
            # return redirect('login')
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('not in group')
                # return redirect('login')
            # elif not group:
                # return view_func(request, *args, **kwargs)
                # return HttpResponse('not have group')
            # elif group == 'vendor':
            #     return redirect('vendor_home')
            # else:
            #     # return HttpResponse(group)
            #     return redirect('login')
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == "shopper":
            return redirect(request.user.groups.all()[0].name)
        elif group == "admin":
            return HttpResponse(request.user.groups.all()[0].name)
    return wrapper_func
