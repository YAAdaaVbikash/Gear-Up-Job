from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from accounts.forms import SeekerSignUpForm, CompanySignUpForm, CompanyForm, UserloginForm, SeekerForm

from accounts.list import category
# Create your views here.


def registerCompany(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        user_form = CompanySignUpForm()
        model_form = CompanyForm()

        if request.method == 'GET':
            return render(request, 'accounts/company_signup.html', {'userform': user_form, 'modelform': model_form})
        else:

            user_form = CompanySignUpForm(request.POST)
            model_form = CompanyForm(request.POST)
            if user_form.is_valid() and model_form.is_valid():
                var_user = user_form.save()
                var_user.is_active = False
                var_user.save()
                var_model = model_form.save(commit=False)
                var_model.company_username = var_user
                var_model.save()
                messages.success(
                    request, 'Your account was created please sent us an email to activate your account')
                return render(request, 'accounts/login.html', {'form': UserloginForm()})
            return render(request, 'accounts/company_signup.html', {'userform': user_form, 'modelform': model_form})


def registerSeeker(request):
    if request.user.is_authenticated:
        return redirect('gearupjob:index')
    else:
        user_form=SeekerSignUpForm()
        model_form=SeekerForm()
        if request.method == 'GET':
#            return render(request,'accounts/signup.html',{'userform':user_form, 'modelform':model_form,'list':catagory})
            return render(request,'accounts/signup.html',{'userform':user_form, 'modelform':model_form})
        else:

            user_form=SeekerSignUpForm(request.POST)
            model_form=SeekerForm(request.POST)

            if user_form.is_valid() and model_form.is_valid():
#            if user_form.is_valid() and model_form.is_valid() and request.POST['catagory']:
                var_user=user_form.save()
                var_user.save()
                var_model=model_form.save(commit=False)
                var_model.seeker=var_user
                var_model.save()
#                var_model.job_category= request.POST['catagory']
#                var_model.save()
                user_name=user_form.cleaned_data.get('username')
                messages.success(request,"Account was Created for "+ user_name)
                return render(request,'accounts/login.html',{'form':UserloginForm()})
            return render(request,'accounts/signup.html',{'userform':user_form, 'modelform':model_form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('gearupjob:index')
    else:
        if request.method == 'GET':
            return render(request, 'accounts/login.html', {'form': UserloginForm()})
        else:
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                messages.success(
                    request, "Username or Password is  incorrect!")
                return render(request, 'accounts/login.html', {'form': UserloginForm()})
            else:
                if user.is_active:
                    login(request, user)
                    return redirect('gearupjob:index')
                else:
                    messages.success(
                        request, "Account not active! Please sent us an email to activate account")
                    return render(request, 'accounts/login.html', {'form': UserloginForm()})


@login_required(login_url='accounts:login')
def user_logout(request):
    if request.method == 'GET':
        logout(request)
    return redirect('accounts:login')
