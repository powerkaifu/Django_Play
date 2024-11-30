'''
序列化器是 Django REST Framework (DRF) 中用於處理數據的橋樑，主要負責：
驗證前端傳入的數據（JSON 格式）。
將數據轉換為後端的 Python 對象，或將後端對象轉為 JSON 格式返回給前端。
'''

from rest_framework import serializers
from .models import UploadImage


# 定義了一個序列化器（Serializer）
class UploadImageSerializer(serializers.ModelSerializer):

  class Meta:
    model = UploadImage  # 指定要被序列化的模型，這是在 models.py 中定義的模型
    fields = '__all__'  # 指定要被序列化的所有欄位
    #  fields = ['image', 'translated_content', 'title'] # 指定要被序列化的模型欄位，這個也是在 models.py 中定義的
