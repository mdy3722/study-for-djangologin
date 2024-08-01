"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from acccounts.views import send_verification_code, verify_code, register_user, login, logout, reset_password
urlpatterns = [
    path('mindary/accounts/original/send-code', send_verification_code, name='send_code'),
    path('mindary/accounts/original/verify-code', verify_code, name='verify_code'),
    path('mindary/accounts/original/register', register_user, name='register_user'),
    path('mindary/accounts/original/login', login, name='original_login'),
    path('mindary/accounts/original/logout', logout, name='original_logout'),
    path('admin/', admin.site.urls),
    path('mindary/accounts/original/reset_password/', reset_password, name='reset_password'),
    #path('api/token/refresh/', token_refresh, name='token_refresh'),
]
