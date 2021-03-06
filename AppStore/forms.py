from django import forms
from django.forms import ModelForm
from .models import User, App, AppCategory

class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=20)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name','nickname', 'password', 'email', 'phone']


class DevRegisterForm(forms.Form):
    fname = forms.CharField(label="FirstName", max_length=20)
    lname = forms.CharField(label="Surname", max_length=20)
    nickname = forms.CharField(label="Nickname", max_length=20)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Phone", max_length=20)
    country = forms.CharField(label="Country", max_length=20)
    company = forms.CharField(label="Company", max_length=20)
    website = forms.CharField(label="Website", max_length=20)
    company_description = forms.CharField(widget=forms.Textarea, label="Company_description")


class NewAppForm(forms.Form):
    name = forms.CharField(label='Name', max_length=20)
    version = forms.CharField(label='Version', max_length=20)
    description = forms.CharField(label='Description', widget=forms.Textarea)
    app_category = forms.ModelChoiceField(queryset=AppCategory.objects.all())

    appImage = forms.ImageField(label="appImage")
    appFile = forms.FileField(label="AppFile")


class NewCategoryForm(forms.Form):
    name = forms.CharField(label='Name', max_length=20)


class AppReviewForm(forms.Form):
    stars = forms.IntegerField(label='Stars', min_value=1, max_value=5)
    text_review = forms.CharField(label='Review', widget=forms.Textarea)


class UpdateAppForm(forms.Form):
    name = forms.CharField(label='Name', max_length=20)
    version = forms.CharField(label='Version', max_length=20)
    description = forms.CharField(label='Description', widget=forms.Textarea)
    app_category = forms.ModelChoiceField(queryset=AppCategory.objects.all())

    appImage = forms.ImageField(label="appImage")
    appFile = forms.FileField(label="AppFile")



class ManageAccount(forms.Form):
    nickname = forms.CharField(label='Nickname', max_length=20, required=True)
    email = forms.EmailField(label='Email', required=True)
    phone = forms.CharField(label='Phone', max_length=20, required=True)
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput, required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)