from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Collections.as_view(), name="Collections"),
    path('<int:pk>/', views.Collections_solo.as_view(), name="collections_solo"),
    
    path('exp/', views.Collections_experimental.as_view(), name="collections_experimental"),
    path('exp/<int:pk>/', views.Collections_solo_experimental.as_view(), name="collections_solo_experimental"),
]