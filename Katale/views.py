from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from .forms import UserRegistrationForm, UserForm
from .models import Users, Category, Product


# Create your views here.


def index(request):
    category_list = Category.objects.order_by('created_at')
    product_list = Product.objects.order_by('created_at')
    # context_dict = {'categories': category_list}
    return render(request, 'Katale/index.html', {'categories': category_list, 'products': product_list})


def account_details(request):

    return render(request, 'Katale/account.html', {})


def product_details(request, product_id):

    category_list = Category.objects.order_by('created_at')

    product = Product.objects.get(pk=product_id)

    return render(request, 'Katale/details.html', {'categories': category_list, 'product': product})


def products(request, category_id):
    category_list = Category.objects.order_by('created_at')

    product = Product.objects.get(pk=product_id)

    return render(request, 'Katale/details.html', {'categories': category_list, 'product': product})


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
            registered = True

            return render_to_response('Katale/index.html', {}, RequestContext(request))
        # else:
        #     print user_profile.is_valid()
        #     print user_profile.errors
            # return HttpResponseRedirect(reverse('Katale:signup'))
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
                return HttpResponseRedirect('/Katale/')

                # return render_to_response('Katale/index.html', {}, RequestContext(request))
            else:
                return HttpResponse('your account is disabled')
                # else:
                #return HttpResponse('Invalid login details provided ')
    else:
        return render(request, 'Katale/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    # return render_to_response('Katale/index.html', {}, RequestContext(request))
    # return render(request, 'Katale/index.html', {})
    return HttpResponseRedirect('/Katale/')

