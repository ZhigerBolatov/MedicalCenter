"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from happylife.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', AuthenticationAPIView.as_view()),
    path('logout/', LogOutAPIView.as_view()),
    path('user/', UserAPIView.as_view()),
    path('reset_password/', PasswordResetAPIView.as_view()),
    path('set_new_password/', SetNewPasswordAPIView.as_view()),
    path('register/', RegistrationAPIView.as_view()),
    path('auth_info/', AuthInfoAPIView.as_view()),
]
