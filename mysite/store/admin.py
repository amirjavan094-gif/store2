from django.contrib import admin
from . import models
from django.contrib.auth.models import User


admin.site.register(models.Category)
admin.site.register(models.Products)

admin.site.register(models.Profile)

class ProfileInLine(admin.StackedInline):
    model = models.Profile


class UserAdmin(admin.ModelAdmin):
    moedl = User
    fields = ['username','first_name','last_name','email']
    inlines = [ProfileInLine ]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


