from django.contrib import admin
from .models import User, App, App_review, AppCategory, Download, Developer

admin.site.register(User)
admin.site.register(App)
admin.site.register(App_review)
admin.site.register(AppCategory)
admin.site.register(Download)
admin.site.register(Developer)