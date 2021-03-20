from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        clean_data = super(UserRegisterForm, self).clean()


class UserLoginForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email']
