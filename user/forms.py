from django import forms
from .models import User


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        return cleaned_data


class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        if not User.objects.filter(email=cleaned_data['email']).exists():
            forms.ValidationError("User is not Exists!!!")
        return cleaned_data
