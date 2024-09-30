from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from account.models import Account, Profile

# Register your models here.
admin.site.register(Profile)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ["email", "role"]

    def save_model(self, request: HttpRequest, obj, form: ModelForm, change: bool):
        super().save_model(request, obj, form, change)
    
        if not Profile.objects.filter(account=obj).exists():
            Profile.objects.create(account=obj)

