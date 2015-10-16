from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from .forms import UserRegistrationForm, UserForm, AddToCartForm
from .models import Users, Category, Product
from Katale import cart


# Create your views here.


def index(request):
    category_list = Category.objects.order_by('created_at')
    # category_list = Category.objects.filter(parent__isnull=True)

    product_list = Product.objects.order_by('created_at')
    if request.method == 'POST':
        if request.user.is_authenticated():
            cart.add_to_cart(request)
        else:
            return render(request, 'Katale/login.html', {})
    cart_item_count = cart.cart_distinct_item_count(request)
    return render(request, 'Katale/index.html', {'categories': category_list, 'products': product_list,
                                                 'cart_count': cart_item_count})


def show_cart(request):
    category_list = Category.objects.order_by('created_at')
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Remove':
            cart.remove_from_cart(request)
    cart_items = cart.get_cart_items(request)
    cart_item_count = cart.cart_distinct_item_count(request)
    return render(request, 'Katale/cart.html', {'products': cart_items, 'cart_count': cart_item_count, 'categories': category_list,})


def account_details(request):
    cart_item_count = cart.cart_distinct_item_count(request)

    return render(request, 'Katale/account.html', {'cart_count': cart_item_count})


def product_details(request, product_id):

    category_list = Category.objects.order_by('created_at')

    product = Product.objects.get(pk=product_id)
    cart_item_count = cart.cart_distinct_item_count(request)
    if request.method == 'POST':
        if request.user.is_authenticated():
            postdata = request.POST.copy()
            form = AddToCartForm(request, postdata)
            if form.is_valid():
                cart.add_to_cart(request)
            # if test cookie worked, get rid of it
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                cart_items = cart.get_cart_items(request)
                return render(request, 'Katale/cart.html', {'products': cart_items, 'cart_count': cart_item_count})
        else:
            return render(request, 'Katale/login.html', {})
    else:
        form = AddToCartForm()
        form.fields['product_id'].widget.attrs['value'] = product_id
        request.session.set_test_cookie()
        return render(request, 'Katale/details.html', {'categories': category_list, 'product': product, 'cart_form': form,
                                                   'cart_count': cart_item_count, })


def products(request, category_id):
    category_list = Category.objects.order_by('created_at')

    product = Product.objects.filter(category_id=category_id)
   # product = Product.objects.filter(sub_category__category_id=category_id)
    cart_item_count = cart.cart_distinct_item_count(request)
    if request.method == 'POST':
        if request.user.is_authenticated():
            cart.add_to_cart(request)
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            cart_items = cart.get_cart_items(request)
            return render(request, 'Katale/cart.html', {'products': cart_items, 'cart_count': cart_item_count})

        else:
            return render(request, 'Katale/login.html', {})
    else:
        return render(request, 'Katale/products.html', {'categories': category_list, 'products': product,
                                                    'cart_count': cart_item_count})


def sign_up(request):
    registered = False
    category_list = Category.objects.order_by('created_at')
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

            userp.save()
            registered = True
            return render(request, 'Katale/index.html', {'categories': category_list})

        else:
            form_errors = user_form.errors
            formm_errors = user_profile.errors
            return render(request, 'Katale/login.html', {'errors': form_errors, 'error': formm_errors, 'user_form': user_form, 'user_profile': user_profile})

    else:
        user_form = UserForm()
        user_profile = UserRegistrationForm()
    return render(request, 'Katale/login.html', {'user_form': user_form, 'user_profile': user_profile, 'categories': category_list})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)


                return HttpResponseRedirect('/Katale/')
            else:
                return render(request, 'Katale/login.html', {})
        else:
            return render(request, 'Katale/login.html', {})

    else:
        return render(request, 'Katale/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/Katale/')

