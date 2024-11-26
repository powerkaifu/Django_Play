# 序列化器（Serializer）在 Django REST framework (DRF) 中扮演著數據轉換和驗證的角色。
# 它們負責將複雜的數據類型（如 Django 模型實例或查詢集）轉換為 Python 原生數據類型，
# 這些數據類型可以輕鬆地轉換為 JSON、XML 或其他內容類型，並且可以將輸入的數據轉換回複雜的數據類型。
# 例如 querysets 和 model instances，轉換為 Python 原生數據類型，以便於 JSON、XML 或其他內容類型的渲染。
from rest_framework import serializers
from .models import UploadImage


# 定義了一個序列化器（Serializer）
class uploadSerializer(serializers.ModelSerializer):

  class Meta:
    model = UploadImage  # 指定要被序列化的模型，這是在 models.py 中定義的模型
    fields = '__all__'  # 指定要被序列化的所有欄位
    # fields = ['image']  # 指定要被序列化的模型欄位，這個也是在 models.py 中定義的
