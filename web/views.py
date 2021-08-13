from django.contrib import auth, messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


# Create your views here.

def login_frm(requests):
    return render(requests, 'login.html')


def do_login(request):
    if request.method == 'POST':
        username = request.POST['login-form-username']
        password = request.POST['login-form-password']

        user = authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # messages.success(request, user.user_type)
            return redirect('technote_frm')

        else:

            messages.error(request, 'Invalid login credentials 007')
            return redirect('login_frm')
    messages.error(request, 'Something is Wrong, Please try again later')
    return redirect('login_frm')


def do_register(request):
    if request.method == 'POST':
        firstname = request.POST['register-form-firstname']
        lastname = request.POST['register-form-lastname']
        email = request.POST['register-form-email']
        username = request.POST['register-form-username']
        password = request.POST['register-form-password']
        repassword = request.POST['register-form-repassword']

        if password != repassword:
            messages.error(request, 'Password does not match')
            return redirect('login_frm')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already used')
            return redirect('login_frm')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered')
            return redirect('login_frm')

        try:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname,
                                            last_name=lastname)
            user.save()
            messages.success(request, 'Successfully registered as ' + request.POST['register-form-username'])
            auth.login(request, user)
            # messages.success(request, user.user_type)
            return redirect('technote_frm')
        except Exception as e:
            messages.error(request, e)
            return redirect('login_frm')

    return None


@login_required(login_url='login_frm')
def technote_frm(request):
    return render(request, 'technote.html')


def log_out(request):
    # messages.success(request, 'you have logged out')
    logout(request)
    return HttpResponseRedirect("/")
