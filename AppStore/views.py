from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from AppStore.forms import LoginForm
from django.template import loader
from django.shortcuts import redirect, render
from .forms import LoginForm, NewAppForm, RegisterForm
from .models import User, App, AppCategory, App_review, Developer, Download

def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            first_select = User.objects.all().filter(email = form.cleaned_data['email'])
            second_select = first_select.filter(password = form.cleaned_data['password'])
            if len(second_select) == 1:
                if(second_select[0].role == 'admin'):
                    return redirect('adminPage')
                elif (second_select[0].role == 'developer'):
                    return redirect('/devPage/' + str(second_select[0].id))
                    # return redirect('/devPage')
                else:
                    return redirect('/userPage/' + str(second_select[0].id))
                    # return redirect('/userPage')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'login.html', {'form': LoginForm()})
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})


def userPage(request, user_id):
    user = User.objects.get(id=user_id)
    appsList = App.objects.all()
    template = loader.get_template('userPage.html')
    context = {
        'appsList': appsList,
        'user': user,
    }
    return HttpResponse(template.render(context, request))


def devPage(request, user_id):
    user = User.objects.get(id=user_id)
    dev = Developer.objects.get(user=user_id)
    devApps = App.objects.all().filter(developer=dev)

    template = loader.get_template('devPage.html')
    context = {
        'dev': dev,
        'devApps': devApps,
        'user': user
    }
    return HttpResponse(template.render(context, request))


def adminPage(request, user_id):
    return render(request, 'adminPage.html')


def appDetail(request, app_id):
    app = App.objects.get(id=app_id)
    return render(request, 'appDetail.html', {'app': app})


def newApp(request, user_id):
    if request.method == 'POST':
        form = NewAppForm(request.POST)
        if form.is_valid():
            dev = Developer.objects.get(user=user_id)

            ## Create new app object fill with form data and dev and save to db
            newApp = App(
                name=form.cleaned_data['name'],
                version=form.cleaned_data['version'],
                description=form.cleaned_data['description'],
                app_category=form.cleaned_data['app_category'],
                developer=dev
            )
            newApp.save()

            return redirect('/devPage/' + str(user_id))
        else:
            return render(request, 'newApp.html', {'form': form})

    else:
        form = NewAppForm()
        return render(request, 'newApp.html', {'form': form})