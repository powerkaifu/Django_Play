# from django.shortcuts import render
# from rest_framework import generics  # 用於繼承API視圖

from .models import UploadImage
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import uploadSerializer
from PIL import Image
import pytesseract
# import openai

# 設置 Tesseract 的執行檔路徑與 OPENAI 的 API 金鑰
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 指定 Tesseract 執行檔的路徑

# openai.api_key = ''


class ImageUploadViewSet(viewsets.ViewSet):
  parser_classes = ( MultiPartParser, FormParser, JSONParser )  # 設置解析器

  # 新增，對應前端的 POST 請求
  def create(self, request, *args, **kwargs):
    serializer = uploadSerializer(data = request.data)  # 將上傳的圖片資料，交給序列化器處理
    if serializer.is_valid():
      upload_image = serializer.save()  # 儲存上傳圖片的圖片路徑，且會回傳一個 UploadImage 實例
      image_path = upload_image.image.path  # 獲取圖片的實體儲存絕對路徑
      image = Image.open(image_path)  # 使用 PIL 打開圖片

      # 進行辨識圖片中的文字
      ocr_text = pytesseract.image_to_string(
          image,
          lang = 'kor+jpn+eng+chi_tra+chi_sim+fra+deu+spa+ita+rus+por+ara+hin+tha+vie',
      )

      # 拿掉換行符號
      ocr_text = ocr_text.replace('\n', ' ')
      # 遇到 . 換行
      ocr_text = ocr_text.replace('. ', '.\n')

      return Response({ 'data': ocr_text, 'id': upload_image.id}, status = status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

  # 更新，對應前端的 PUT 請求
  def update(self, request, *args, **kwargs):
    try:
      data = request.data.get('data')
      upload_image = UploadImage.objects.get(id = kwargs.get('pk'))
      upload_image.edit_content = data
      upload_image.save()
      return Response({ 'message': '更新成功'}, status = status.HTTP_200_OK)
    except UploadImage.DoesNotExist:
      return Response({ 'error': '未找到對應的記錄'}, status = status.HTTP_404_NOT_FOUND)
    except Exception as e:
      return Response({ 'error': str(e)}, status = status.HTTP_400_BAD_REQUEST)
