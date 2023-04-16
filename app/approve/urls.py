from django.contrib import admin
from django.urls import path, include
from .models import Non_approved
from . import views

urlpatterns = [
    path('', views.imp, name="import"),
    path('non_approved/', views.NonApproved.as_view(), name="non_approved"),
    path('non_approved/<int:pk>/', views.Folder.as_view(), name="folder"),
    path('export/', views.ExportCSV.as_view(), name="export"),
]
