'''
序列化器是 Django REST Framework (DRF) 中用於處理數據的橋樑，
主要負責前後端資料格式的轉換：
1. 驗證前端傳入的數據（JSON 格式），將數據轉換為後端的 Python 對象。
2. 或將後端對象轉為 JSON 格式返回給前端。
'''

from rest_framework import serializers
from .models import UploadImage


# 自定義序列化器（Serializer）
class UploadImageSerializer(serializers.ModelSerializer):

  class Meta:
    model = UploadImage  # 被序列化的模型
    fields = '__all__'  # 被序列化的所有欄位

  def validate_title(self, value):
    if not value:
        return '未填入標題'
    return value