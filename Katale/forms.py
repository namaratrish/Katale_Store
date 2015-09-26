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
    #birthdate = forms.DateField(widget=forms.TextInput(attrs=dict({'placeholder': 'yyyy-mm-dd'}, required=True)),)
    birthdate = forms.DateField(widget=SelectDateWidget(years = range(2015, 1950, -1)))

    class Meta:
        model = Users
        fields = ['city', 'address', 'phone_number', 'birthdate']
