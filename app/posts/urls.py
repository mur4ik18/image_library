from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.Posts_page.as_view(), name="page")
]