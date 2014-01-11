from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class Accounts(models.Model):
    Login = models.OneToOneField(User,primary_key=True)
    GGNumber = models.DecimalField(max_digits=19,decimal_places=0)
    FacebookId = models.CharField(max_length=100)

class AccountsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User',               {'fields': ['Login']}),
        ('Account information', {'fields': ['GGNumber','FacebookId'],'classes': ['collapse']}),
    ]
    list_display = ('Login', 'GGNumber', 'FacebookId')

admin.site.register(Accounts,AccountsAdmin)