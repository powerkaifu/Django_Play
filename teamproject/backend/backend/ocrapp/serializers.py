'''
序列化器是 Django REST Framework (DRF) 中用於處理數據的橋樑，
主要負責前後端資料格式的轉換：
1. 驗證前端傳入的數據（JSON 格式），將數據轉換為後端的 Python 對象。
2. 或是將後端對象轉為 JSON 格式返回給前端。
'''

from rest_framework import serializers
from .models import UploadImage

# 自定義序列化器（Serializer）
class UploadImageSerializer(serializers.ModelSerializer):
  # 內嵌類別 Meta：配置序列化器的元數據
  class Meta:
    model = UploadImage  # 被序列化的模型
    fields = '__all__'  # 被序列化的所有欄位

  # 指定 title 欄位的驗證規則
  title = serializers.CharField(
        required=True,
        error_messages={
            'required': '必須填寫此欄位',
            'blank': '欄位不可為空白!!!',
        }
  )

  # 自定義驗證方法，驗證 title 的標題長度
  def validate_title(self, value):
    if len(value) < 3:
        raise serializers.ValidationError("標題長度必須至少 3 個字符")
    return value