from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from .forms import UserRegistrationForm, UserForm
from .models import Users


# Create your views here.


def index(request):
    return render(request, 'Katale/index.html', {})


def account_details(request):
    return render(request, 'Katale/account.html', {})


def sign_up(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_profile = UserRegistrationForm(request.POST)
        if user_form.is_valid() and user_profile.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            userp = Users(user=user, city=user_profile.cleaned_data['city'],
                          address=user_profile.cleaned_data['address'],
                          birthdate=user_profile.cleaned_data['birthdate'],
                          phone_number=user_profile.cleaned_data['phone_number'])
            # userp = user_profile.save(commit=False)

            # userp.user = user
            userp.save()
            registered=True

            return render_to_response('Katale/index.html', {}, RequestContext(request))
        else:
            print user_form.errors, user_profile.errors
    else:
        user_form = UserForm()
        user_profile = UserRegistrationForm()
        return render(request, 'Katale/login.html', {'user_form': user_form, 'user_profile': user_profile})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # return HttpResponseRedirect('/Tunda/index/')

                return render_to_response('Katale/index.html', {}, RequestContext(request))
            else:
                return HttpResponse('your account is disabled')
        #else:
            #return HttpResponse('Invalid login details provided ')
    else:
        return render(request, 'Katale/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return render_to_response('Katale/index.html', {}, RequestContext(request))

