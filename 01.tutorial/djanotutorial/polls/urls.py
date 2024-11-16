# 新增一個路由，用於定義 polls 應用的 URL 模式

from django.urls import path
from . import views

app_name = 'polls'  # 為這個應用添加命名空間
urlpatterns = [
    # ex: /polls/
    path('', views.index, name = 'index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name = 'detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name = 'results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name = 'vote')
]
