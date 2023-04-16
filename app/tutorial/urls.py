"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from auth_system import views
from . import views

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),   
    # posts
    path('post/', include('posts.urls')),
    # collections
    path('collection/', include('posts_collections.urls')),
    # writers
    path('writer/', include('writers.urls')),
    # search
    path('search/', include('advanced_search.urls')),

    # import
    path('import/', include('approve.urls')),

    path('__debug__/', include('debug_toolbar.urls')),

    path('api/', include('api.urls')),
    # login
    path('accounts/', include('auth_system.urls')),
    
    path('api2/', include('apiapp.urls')),

    path('', views.home_page, name='home_page')
]
if bool(settings.DEBUG):
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)