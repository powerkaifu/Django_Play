# from django.shortcuts import render
# from rest_framework import generics  # 用於繼承API視圖

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UploadImage
from .serializers import uploadSerializer
from PIL import Image
import pytesseract
# import openai

# 指定 Tesseract 執行檔的路徑
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 設置 OpenAI API 密鑰
# openai.api_key = 'your_openai_api_key'


class ImageUploadViewSet(viewsets.ViewSet):
  # parser_classes = ( MultiPartParser, FormParser )

  def create(self, request, *args, **kwargs):
    serializer = uploadSerializer(data = request.data)  # 將上傳的圖片資料，交給序列化器處理

    if serializer.is_valid():
      upload_image = serializer.save()  # 將上傳的圖片，儲存它的圖片路徑，會回傳一個 UploadImage 實例
      image_path = upload_image.image.path  # 獲取圖片的實體儲存絕對路徑
      image = Image.open(image_path)  # 使用 PIL 打開圖片
      ocr_text = pytesseract.image_to_string(image)  # 使用 Tesseract 進行 OCR 文字識別
      # text = text.replace('\n', ' ').strip() # 去除多餘的換行符
      # print(ocr_text)
      return Response({ 'data': ocr_text}, status = status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
