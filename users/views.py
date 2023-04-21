from django.shortcuts import render,HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import UserRegistrationModel
from django.conf import settings
from django.http import JsonResponse
import os
import pandas as pd
from django.http import FileResponse
# from django.shortcuts import get_object_or_404
from django.http import Http404


# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})

def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginname')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHome.html', {})
            elif status == "deactivated":
                messages.success(request, 'Your Account has been deactivated.')
                return render(request, 'UserLogin.html')
            else:
                messages.success(request, 'Your Account has not been activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})

def UserHome(request):
    return render(request, 'users/UserHome.html', {})

def usersViewDataset(request):
    # dataset_path = os.path.join(settings.MEDIA_ROOT, 'Shanghai_data.csv')
    # df = pd.read_csv(dataset_path)

    # next_days = list(df['day1'].iloc[1:])
    # next_days.append(79)
    # df['nextDay'] = next_days

    # df['nextDay'] = df['nextDay'].astype(int)

    # df.to_csv('Shanghai_data.csv', index=False)

    dataset_path = os.path.join(settings.MEDIA_ROOT, 'Shanghai_data.csv')
    df = pd.read_csv(dataset_path)

    df = df.to_html(index=None)
    return render(request, 'users/viewData.html',{'data': df})


def lassoResults(request):
    from .utility import LassoUtility
    data = LassoUtility.simple_linear_regression()
    ls_mae,ls_mse = LassoUtility.lasso_regression()
    l_mae,l_mse = LassoUtility.kernel_my_lasso()
    return render(request, 'users/ml_results.html',{'ls_mae': ls_mae,'ls_mse': ls_mse,'l_mae': l_mae, 'l_mse': l_mse})

def userPrediction(request):
    if request.method == 'POST':
        day1 = float(request.POST.get('day1'))
        day2 = float(request.POST.get('day2'))
        day3 = float(request.POST.get('day3'))
        day4 = float(request.POST.get('day4'))
        day5 = float(request.POST.get('day5'))
        day6 = float(request.POST.get('day6'))
        day7 = float(request.POST.get('day7'))
        model_file = os.path.join(settings.MEDIA_ROOT, 'model.alex')
        test_set = [day1, day2, day3, day4, day5, day6, day7]
        import pickle
        model = pickle.load(open(model_file,'rb'))
        pred = model.predict([test_set])
        print("===>", pred)
        response_data = {'prediction': pred.tolist()}
        print(f'\n\nType of data.tolist() is : {type(pred.tolist())}\n\n')
        print(pred.tolist())
        return JsonResponse(response_data)
    else:
        return render(request, 'users/predictForm.html',{})

def userForeCast(request):
    # from .utility.forecastanalysis import start_forecasting
    # forecast_values = start_forecasting()
    # pred_ci = forecast_values.to_html
    # return render(request, 'users/forecast.html',{'data': pred_ci})

    with open('my_forecast.html', 'r') as f:
        forecast_table = f.read()
    return render(request, 'users/forecast.html', {'data': forecast_table})

def download_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    raise Http404

