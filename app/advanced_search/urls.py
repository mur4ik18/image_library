from django.urls import path
from . import views

urlpatterns = [
    path('', views.Search_main.as_view(), name='search'),
    path('search/', views.Search.as_view(), name='search_search')
]
