from django.forms.extras import SelectDateWidget

__author__ = 'LT10'

from django import forms
from django.core.exceptions import ValidationError
from .models import Users
from django.forms import ModelForm
from django.contrib.auth.models import User

BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def __init__(self, data={}):
        super(UserForm, self).__init__(data=data)
        self.fields['password_again'] = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True)))

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        if cleaned_data.get('password') != cleaned_data.get('password_again'):
            raise ValidationError('Password Mismatch')
        else:
            return cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username already taken, please choose another')


class UserRegistrationForm(ModelForm):
    city = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label="City")
    address = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label="Address")
    phone_number = forms.IntegerField(widget=forms.TextInput(attrs=dict(max_length=15, required=True)))
    birthdate = forms.DateField(widget=SelectDateWidget)

    class Meta:
        model = Users
        fields = ['city', 'address', 'phone_number', 'birthdate']


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        widget=forms.TextInput(attrs={'size': '2', 'max_length': '5', 'value': '1', 'class': 'quantity'}),
        error_messages={'invalid': 'Please enter a valid quantity'}, min_value=1)
    product_id = forms.IntegerField(widget=forms.HiddenInput())

    # override the default __init__ so we can set the request
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(AddToCartForm, self).__init__(*args, **kwargs)

    # custom validation to check for cookies
    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError('Cookies must be enabled on your computer')
            return self.cleaned_data


