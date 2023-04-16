from django.contrib import admin
from .models import *
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'for_changing')

admin.site.register(Collection, AuthorAdmin)