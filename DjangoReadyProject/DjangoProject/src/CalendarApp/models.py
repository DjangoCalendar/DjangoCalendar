from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class Accounts(models.Model):
    Login = models.OneToOneField(User,primary_key=True)
    GGNumber = models.DecimalField(max_digits=19,decimal_places=0)
    FacebookId = models.CharField(max_length=100)
    AvatarId = models.CharField(max_length=100,default='av2.jpg')

class AccountsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User',               {'fields': ['Login']}),
        ('Account information', {'fields': ['GGNumber','FacebookId','AvatarId'],'classes': ['collapse']}),
    ]
    list_display = ('Login', 'GGNumber', 'FacebookId','AvatarId')

admin.site.register(Accounts,AccountsAdmin)

class Entry(models.Model):
    title = models.CharField(max_length=40)
    snippet = models.CharField(max_length=150, blank=True)
    body = models.TextField(max_length=10000, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField(blank=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    remind = models.BooleanField(default=False)

    def __unicode__(self):
        if self.title:
            return unicode(self.creator) + u" - " + self.title
        else:
            return unicode(self.creator) + u" - " + self.snippet[:40]

    def short(self):
        if self.snippet:
            return "<i>%s</i> - %s" % (self.title, self.snippet)
        else:
            return self.title
    short.allow_tags = True

    class Meta:
        verbose_name_plural = "entries"


### Admin

class EntryAdmin(admin.ModelAdmin):
    list_display = ["creator", "date", "title", "snippet"]
    list_filter = ["creator"]

admin.site.register(Entry, EntryAdmin)