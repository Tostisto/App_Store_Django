from pydoc import describe
from statistics import mode
from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=20, unique=True)
    phone = models.CharField(max_length=20, unique=True)
    register_date = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, default='user')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class App(models.Model):
    name = models.CharField(max_length=20)
    version = models.CharField(max_length=20)
    description = models.TextField()
    app_category = models.ForeignKey('AppCategory', on_delete=models.CASCADE)
    developer = models.ForeignKey('Developer', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class App_review(models.Model):
    stars = models.IntegerField()
    text_review = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)

    def __str__(self):
        return self.text_review


class AppCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Download(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' ' + self.app.name

class Developer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=20)
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


