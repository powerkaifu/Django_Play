"""
URL configuration for mysite project.

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

# 這裡是 mysite 的 URLconf(主路由)，用於將其他應用的 URLconf 包含進來
from django.contrib import admin
from django.urls import path, include  # include 用於引用其他應用的 URLconf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),  # 這裡將 polls/ URLconf 包含進來
]
