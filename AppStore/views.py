import os
from django.conf import settings
from django.shortcuts import render
from django.http import Http404, HttpResponse
from AppStore.forms import LoginForm
from django.template import loader
from django.shortcuts import redirect, render
from .forms import AppReviewForm, DevRegisterForm, LoginForm, NewAppForm, RegisterForm, NewCategoryForm, UpdateAppForm, ManageAccount
from .models import User, App, AppCategory, App_review, Developer, Download


def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            first_select = User.objects.all().filter(
                email=form.cleaned_data['email'])
            second_select = first_select.filter(
                password=form.cleaned_data['password'])
            if len(second_select) == 1:
                if(second_select[0].role == 'admin'):
                    request.session['userId'] = second_select[0].id # Session
                    return redirect('/adminPage')
                elif (second_select[0].role == 'developer'):
                    request.session['userId'] = second_select[0].id # Session
                    return redirect('/devPage')
                else:
                    request.session['userId'] = second_select[0].id # Session
                    return redirect('/userPage')
    else:
        form = LoginForm()

    return render(request, 'AppStore/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, 'AppStore/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'AppStore/register.html', {'form': form})

def logout(request):
    del request.session['userId']
    return redirect('/')


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
                country=form.cleaned_data['country'],
                company=form.cleaned_data['company'],
                website=form.cleaned_data['website'],
                company_description=form.cleaned_data['company_description'],
                )
            newDev.save()

            return redirect('/')

        else:
            return render(request, 'AppStore/devRegister.html', {'form': form})
    else:
        form = DevRegisterForm()
        return render(request, 'AppStore/devRegister.html', {'form': form})


def userPage(request):
    user =  User.objects.get(id=request.session['userId'])

    if(user.role != 'user'):
        del request.session['userId']
        return redirect('/')

    appsList = App.objects.all()
    template = loader.get_template('AppStore/userPage.html')
    context = {
        'appsList': appsList,
        'user': user,
    }
    return HttpResponse(template.render(context, request))


def devPage(request):
    user = User.objects.get(id=request.session['userId'])

    if user.role != 'developer':
        del request.session['userId']
        return redirect('/')

    dev = Developer.objects.get(user=user.id)
    devApps = App.objects.all().filter(developer=dev)

    template = loader.get_template('AppStore/devPage.html')
    context = {
        'dev': dev,
        'devApps': devApps,
        'user': user
    }
    return HttpResponse(template.render(context, request))


def adminPage(request):
    admin = User.objects.get(id=request.session['userId'])

    if admin.role != 'admin':
        del request.session['userId']
        return redirect('/')

    allDevs = Developer.objects.all()
    allUsers = User.objects.all().filter(role='user')
    allApps = App.objects.all()

    template = loader.get_template('AppStore/adminPage.html')
    context = {
        'user': admin,
        'devs': allDevs,
        'apps': allApps,
        'users': allUsers,
        'admin': admin
    }
    return HttpResponse(template.render(context, request))


def newApp(request):
    user = User.objects.get(id=request.session['userId'])
    if user.role != 'developer':
        del request.session['userId']
        return redirect('/')

    if request.method == 'POST':
        form = NewAppForm(request.POST, request.FILES)

        if form.is_valid():
            user = User.objects.get(id=request.session['userId']) 
            dev = Developer.objects.get(user=user.id)
            newApp = App(
                name=form.cleaned_data['name'],
                version=form.cleaned_data['version'],
                description=form.cleaned_data['description'],
                app_category=form.cleaned_data['app_category'],
                developer=dev,
                appImage = form.cleaned_data['appImage'],
                appFile = form.cleaned_data['appFile']
            )
            newApp.save()

            return redirect('/devPage')
        else:
            return render(request, 'AppStore/newApp.html', {'form': form})

    else:
        user = User.objects.get(id=request.session['userId']) 
        form = NewAppForm()
        return render(request, 'AppStore/newApp.html', {'form': form, 'user': user})


def appDetail(request, app_id):
    app = App.objects.get(id=app_id)
    user = User.objects.get(id=request.session['userId'])
    reviews = App_review.objects.all().filter(app=app)

    if request.method == 'POST':
        form = AppReviewForm(request.POST)
        if form.is_valid():
            newReview = App_review(
                app=app,
                user=user,
                text_review=form.cleaned_data['text_review'],
                stars=form.cleaned_data['stars']
            )
            newReview.save()
            return redirect('/appDetail/' + str(app_id))
        else:
            return render(request, 'AppStore/appDetail.html', {'form': form, 'app': app, 'user': user, 'reviews': reviews})
    else:
        form = AppReviewForm()
        return render(request, 'AppStore/appDetail.html', {'form': form, 'app': app, 'user': user, 'reviews': reviews})


def removeApp(request, app_id):
    user = User.objects.get(id=request.session['userId'])
    if user.role != 'admin':
        del request.session['userId']
        return redirect('/')

    app = App.objects.get(id=app_id)
    app.delete()
    return redirect('/adminPage')


def removeUser(request, user_id):
    user = User.objects.get(id=request.session['userId'])
    if user.role != 'admin':
        del request.session['userId']
        return redirect('/')

    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('/adminPage')


def removeDev(request, dev_id):
    user = User.objects.get(id=request.session['userId'])
    if user.role != 'admin':
        del request.session['userId']
        return redirect('/')


    dev = Developer.objects.get(id=dev_id)
    dev.delete()
    return redirect('/adminPage')


def installApp(request, app_id):
    if 'userId' not in request.session:
        return redirect('/')


    app = App.objects.get(id=app_id)
    user = User.objects.get(id=request.session['userId'])

    newDownload = Download(
        app=app,
        user=user
    )
    newDownload.save()

    return redirect("/media/" + str(app.appFile))


def manageCategory(request):
    user = User.objects.get(id=request.session['userId'])
    if user.role != 'admin':
        del request.session['userId']
        return redirect('/')

    categories = AppCategory.objects.all()
    return render(request, 'AppStore/manageCategory.html', {'categories': categories})


def removeCategory(request, category_id):
    user = User.objects.get(id=request.session['userId'])
    if user.role != 'admin':
        del request.session['userId']
        return redirect('/')

    category = AppCategory.objects.get(id=category_id)
    category.delete()
    return redirect('/adminPage/manageCategory')


def newCategory(request):
    user = User.objects.get(id=request.session['userId'])
    if user.role != 'admin':
        del request.session['userId']
        return redirect('/')

    if request.method == 'POST':
        form = NewCategoryForm(request.POST)
        if form.is_valid():
            newCat = AppCategory(
                name=form.cleaned_data['name']
            )
            newCat.save()

            return redirect('/adminPage/manageCategory')
        else:
            return render(request, 'AppStore/newCategory.html', {'form': form})

    else:
        form = NewCategoryForm()
        return render(request, 'AppStore/newCategory.html', {'form': form})


def updateApp(request, app_id):
    app = App.objects.get(id=app_id)
    user = User.objects.get(id=request.session['userId'])

    if user.role != 'developer':
        del request.session['userId']
        return redirect('/')

    if request.method == 'POST':
        form = UpdateAppForm(request.POST, request.FILES)
        if form.is_valid():
            app.name = form.cleaned_data['name']
            app.version = form.cleaned_data['version']
            app.description = form.cleaned_data['description']
            app.app_category = form.cleaned_data['app_category']

            app.appImage = form.cleaned_data['appImage']

            app.appFile = form.cleaned_data['appFile']

            app.save()

            return redirect('/devPage')
        else:
            return render(request, 'AppStore/updateApp.html', {'form': form, 'app': app, 'user': user})

    else:
        form = UpdateAppForm( initial= {
            'name': app.name,
            'version': app.version,
            'description': app.description,
            'app_category': app.app_category
        })
        return render(request, 'AppStore/updateApp.html', {'form': form, 'app': app, 'user': user})


def manageAccount(request):
    if 'userId' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['userId'])

    if request.method == 'POST':
        form = ManageAccount(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['password']

            user.nickname = nickname
            user.email = email
            user.phone = phone

            if user.password == old_password:
                if len(new_password) > 4:
                    user.password = new_password
                    user.save() 
                else:
                    form.add_error('password', 'Password must be at least 5 characters')
                    return render(request, 'manageAccount.html', {'form': form, 'user': user})
            else:
                user.save()
            
            return redirect('/userPage')
        else:
            return render(request, 'AppStore/manageAccount.html', {'form': form, 'user': user})

    else:
        form = ManageAccount(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'nickname': user.nickname,
            'email': user.email,
            'phone': user.phone,
            'password': user.password
        })
        return render(request, 'AppStore/manageAccount.html', {'form': form, 'user': user})

def manageAccountDev(request):
    if 'userId' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['userId'])

    if request.method == 'POST':
        form = ManageAccount(request.POST)
        if form.is_valid():
            user.nickname = form.cleaned_data['nickname']
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']

            if user.password != form.cleaned_data['old_password']:
                user.save()
            else:
                user.password = form.cleaned_data['password']
                user.save()
            
            return redirect('/devPage')
        else:
            return render(request, 'AppStore/manageAccount.html', {'form': form, 'user': user})

    else:
        form = ManageAccount(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'nickname': user.nickname,
            'email': user.email,
            'phone': user.phone,
            'password': user.password
        })
        return render(request, 'AppStore/manageAccount.html', {'form': form, 'user': user})

def devRemoveApp(request, app_id):
    user = User.objects.get(id=request.session['userId'])
    
    if user.role != 'developer':
        del request.session['userId']
        return redirect('/')

    app = App.objects.get(id=app_id)
    app.delete()
    return redirect('/devPage')

def media(request, path):
    if 'userId' not in request.session:
        return redirect('/')

    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def downloadedApps(request):
    if 'userId' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['userId'])

    downloadedApps = Download.objects.filter(user=user)

    return render(request, 'AppStore/downloadedApps.html', {'downloadedApps': downloadedApps})

