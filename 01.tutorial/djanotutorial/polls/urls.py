# 新增一個路由，用於定義 polls 應用的 URL 模式

from django.urls import path
from . import views

app_name = 'polls'  # 為這個應用添加命名空間
# urlpatterns = [
#     path('', views.index, name = 'index'),  # ex: /polls/
#     path('<int:question_id>/', views.detail, name = 'detail'),  # ex: /polls/5/
#     path('<int:question_id>/results/', views.results, name = 'results'),  # ex: /polls/5/results/
#     path('<int:question_id>/vote/', views.vote, name = 'vote')  # ex: /polls/5/vote/
# ]

# 改良後的路由
urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    path('<int:pk>/', views.DetailView.as_view(), name = 'detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name = 'results'),
    path('<int:question_id>/vote/', views.vote, name = 'vote')
]
