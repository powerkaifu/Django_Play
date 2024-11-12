# 新增一個路由，用於定義 polls 應用的 URL 模式

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
]
