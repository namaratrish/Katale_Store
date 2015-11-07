from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from .forms import UserRegistrationForm, UserForm, AddToCartForm, CategoryForm, ProductForm
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
        if postdata['submit'] == 'Update':
            cart.update_cart(request)
    cart_items = cart.get_cart_items(request)
    cart_item_count = cart.cart_distinct_item_count(request)
    cart_subtotal = cart.cart_total_price(request)
    # final_price = cart.cart_total_price(request)
    return render(request, 'Katale/cart.html',
                  {'products': cart_items, 'cart_count': cart_item_count, 'categories': category_list,
                   'sub_total': cart_subtotal})


def account_details(request):
    cart_item_count = cart.cart_distinct_item_count(request)

    return render(request, 'Katale/account.html', {'cart_count': cart_item_count})


def product_details(request, product_id):
    category_list = Category.objects.order_by('created_at')

    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        if request.user.is_authenticated():
            postdata = request.POST.copy()
            form = AddToCartForm(request, postdata)
            if form.is_valid():
                cart.add_to_cart(request)
                # if test cookie worked, get rid of it
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

        else:
            return render(request, 'Katale/login.html', {})
    else:
        form = AddToCartForm()
        form.fields['product_id'].widget.attrs['value'] = product_id
        request.session.set_test_cookie()
    cart_item_count = cart.cart_distinct_item_count(request)
    return render(request, 'Katale/details.html', {'categories': category_list, 'product': product, 'cart_form': form,
                                                   'cart_count': cart_item_count, })


def products(request, category_id):
    category_list = Category.objects.order_by('created_at')

    product = Product.objects.filter(category_id=category_id)
    # product = Product.objects.filter(sub_category__category_id=category_id)

    if request.method == 'POST':
        if request.user.is_authenticated():
            cart.add_to_cart(request)
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
                # cart_items = cart.get_cart_items(request)
                # return render(request, 'Katale/cart.html', {'products': cart_items, 'cart_count': cart_item_count})
        else:
            return render(request, 'Katale/login.html', {})

    cart_item_count = cart.cart_distinct_item_count(request)
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
            registration_message = "You have been registered successfully"
            return render(request, 'Katale/login.html', {'user_form': user_form, 'user_profile': user_profile,
                                                         'categories': category_list, 'registered': registered,
                                                         'message': registration_message})

        else:
            form_errors = user_form.errors
            formm_errors = user_profile.errors
            return render(request, 'Katale/login.html',
                          {'errors': form_errors, 'error': formm_errors, 'user_form': user_form,
                           'user_profile': user_profile})

    else:
        user_form = UserForm()
        user_profile = UserRegistrationForm()
    return render(request, 'Katale/login.html',
                  {'user_form': user_form, 'user_profile': user_profile, 'categories': category_list})


def admin(request):
    category_list = Category.objects.order_by('created_at')
    product_list = Product.objects.all()
    category_form = CategoryForm()
    product_form = ProductForm()
    if request.user.is_authenticated():
        if request.method == 'POST':
            post_data = request.POST.copy()
            if post_data['submit'] == 'category':
                category_form = CategoryForm(request.POST)
                if category_form.is_valid():
                    category_form.save()
                    # message = 'Category added'
                    return render(request, 'Katale/admin.html', {})
                else:
                    error_form = category_form.errors
                    return render(request, 'Katale/admin.html', {'errors': error_form, 'category_form': category_form,
                                                                 'categories': category_list, 'products': product_list})
            if post_data['submit'] == 'product':
                product_form = ProductForm(request.POST, request.FILES)
                if product_form.is_valid():
                    product_form.save()
                    return render(request, 'Katale/login.html', {})
                else:
                    error_form = product_form.errors
                    return render(request, 'Katale/admin.html', {'errors': error_form, 'product_form': product_form,
                                                                 'categories': category_list, 'products': product_list})
            if post_data['submit'] == 'DeleteCategory':
                if request.method == 'POST':
                    categories_list = request.POST.getlist('categories')
                    for category in categories_list:
                        x = Category.objects.filter(category=category)
                        x.delete()
            if post_data['submit'] == 'DeleteProduct':
                product_id = post_data['product_id']
                product = Product.objects.filter(pk=product_id)
                product.delete()
            if post_data['submit'] == 'UpdateQuantity':
                product_id = post_data['product_id']
                quantity = int(post_data['quantity'])
                product = Product.objects.filter(pk=product_id)
                for x in product:
                    x.quantity = quantity
                    x.save()
            if post_data['submit'] == 'UpdatePrice':
                product_id = post_data['product_id']
                price = int(post_data['price'])
                product = Product.objects.filter(pk=product_id)
                for x in product:
                    x.price = price
                    x.save()
        else:
            return render(request, 'Katale/admin.html', {'category_form': category_form, 'product_form': product_form,
                                                         'categories': category_list, 'products': product_list})
    else:
        user_form = UserForm()
        user_profile = UserRegistrationForm()
        return render(request, 'Katale/login.html',
                      {'user_form': user_form, 'user_profile': user_profile, 'categories': category_list})


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
            message = 'Invalid username or password.'
            return render(request, 'Katale/login.html', {'message': message})
    else:
        return render(request, 'Katale/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/Katale/')

