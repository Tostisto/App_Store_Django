from django import forms
from django.forms import ModelForm
from .models import User, App, AppCategory

class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=20)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','nickname', 'password', 'email', 'phone']


class NewAppForm(forms.Form):
    name = forms.CharField(label='Name', max_length=20)
    version = forms.CharField(label='Version', max_length=20)
    description = forms.CharField(label='Description', widget=forms.Textarea)
    app_category = forms.ModelChoiceField(queryset=AppCategory.objects.all())