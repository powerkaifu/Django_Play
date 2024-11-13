# 設定後台管理的功能

from django.contrib import admin  # 默認的管理員應用
from .models import Question, Choice  # 引入 Question、Choice 模型
# Register your models here.

admin.site.register(Question)  # 註冊 Question 模型，可以在後台管理介面中看到 Question 模型的資料
admin.site.register(Choice)
