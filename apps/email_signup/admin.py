from django.contrib import admin

# Register your models here.
from .models.email import email


class EmailAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__']


admin.site.register(email, EmailAdmin)
