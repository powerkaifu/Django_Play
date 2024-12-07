from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageUploadViewSet

router = DefaultRouter()  # 配置 DRF 的 DefaultRouter

## r'upload'：路由的前綴，例如 http://127.0.0.1:8000/api/upload/
router.register(r'upload', ImageUploadViewSet, basename = 'upload')  # 註冊路由

urlpatterns = [
    path('', include(router.urls)),
]
