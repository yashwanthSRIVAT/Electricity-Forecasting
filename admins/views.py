from django.shortcuts import render,HttpResponse
from django.contrib import messages
from users.models import UserRegistrationModel

# Create your views here.

def AdminLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("User ID is = ", usrid)
        if usrid == 'admin' and pswd == 'admin':
            return render(request, 'admins/AdminHome.html')
        elif usrid == 'Admin' and pswd == 'Admin':
            return render(request, 'admins/AdminHome.html')
        else:
            messages.success(request, 'Please Check Your Login Details')
    return render(request, 'AdminLogin.html', {})


def AdminHome(request):
    return render(request, 'admins/AdminHome.html')


def ViewRegisteredUsers(request):
    data = UserRegistrationModel.objects.all()
    return render(request, 'admins/RegisteredUsers.html', {'data': data})


def AdminActivaUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        UserRegistrationModel.objects.filter(id=id).update(status=status)
        data = UserRegistrationModel.objects.all()
        return render(request, 'admins/RegisteredUsers.html', {'data': data})


def adminResults(request):
    from users.utility import LassoUtility
    data = LassoUtility.simple_linear_regression()
    ls_mae, ls_mse = LassoUtility.lasso_regression()
    l_mae, l_mse = LassoUtility.kernel_my_lasso()
    return render(request, 'admins/results.html',
                  {'ls_mae': ls_mae, 'ls_mse': ls_mse, 'l_mae': l_mae, 'l_mse': l_mse})
