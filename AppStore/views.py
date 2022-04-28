from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from AppStore.forms import LoginForm
from django.template import loader
from django.shortcuts import redirect, render
from .forms import DevRegisterForm, LoginForm, NewAppForm, RegisterForm
from .models import User, App, AppCategory, App_review, Developer, Download

def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            first_select = User.objects.all().filter(email = form.cleaned_data['email'])
            second_select = first_select.filter(password = form.cleaned_data['password'])
            if len(second_select) == 1:
                if(second_select[0].role == 'admin'):
                    return redirect('/adminPage/' + str(second_select[0].id))
                elif (second_select[0].role == 'developer'):
                    return redirect('/devPage/' + str(second_select[0].id))
                else:
                    return redirect('/userPage/' + str(second_select[0].id))
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


def devRegister(request):
    if request.method == 'POST':
        form = DevRegisterForm(request.POST)
        if form.is_valid():
            
            newUse = User(
                first_name=form.cleaned_data['fname'],
                last_name=form.cleaned_data['lname'],
                nickname=form.cleaned_data['nickname'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                role='developer'
            )

            newUse.save()

            newDev = Developer(
                user_id=newUse.id,
                country=form.cleaned_data['Country']
            )
            newDev.save()

            return render(request, 'login.html', {'form': LoginForm()})

        else:
            return render(request, 'devRegister.html', {'form': form})
    else:
        form = DevRegisterForm()
        return render(request, 'devRegister.html', {'form': form})



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
    admin = User.objects.get(id=user_id)
    allDevs = Developer.objects.all()
    allUsers = User.objects.all().filter(role = 'user')
    allApps = App.objects.all()

    template = loader.get_template('adminPage.html')
    context = {
        'devs': allDevs,
        'apps': allApps,
        'users': allUsers,
        'admin': admin
    }
    return HttpResponse(template.render(context, request))

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


def appDetail(request, app_id, user_id):
    # return render(request, 'appDetail.html')
    app = App.objects.filter(id=app_id)[0]
    user = User.objects.get(id=user_id)

    template = loader.get_template('appDetail.html')
    context = {
        'app': app,
        'user': user
    }
    return HttpResponse(template.render(context, request))


def removeApp(request, app_id):
    app = App.objects.get(id=app_id)
    app.delete()
    return redirect('/adminPage/' + str(request.user.id))

def removeUser(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('/adminPage/' + str(request.user.id))

def removeDev(request, dev_id):
    dev = Developer.objects.get(id=dev_id)
    dev.delete()
    return redirect('/adminPage/' + str(request.user.id))


def installApp(request, app_id, user_id):
    app = App.objects.get(id=app_id)
    user = User.objects.get(id=user_id)

    newDownload = Download(
        app=app,
        user=user
    )
    newDownload.save()

    return redirect('/userPage/' + str(user_id))