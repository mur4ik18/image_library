
from . import views 
from django.urls import path, include

urlpatterns = [ 
    path('ai_texts/', views.ai_texts),
]