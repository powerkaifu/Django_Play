# from django.shortcuts import render
# from rest_framework import generics  # 用於繼承API視圖

from .models import UploadImage
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action
from .serializers import UploadImageSerializer
from PIL import Image
import pytesseract
import openai

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 指定 Tesseract 執行檔的路徑

class ImageUploadViewSet(viewsets.ViewSet):
  parser_classes = ( MultiPartParser, FormParser, JSONParser )  # 設置解析器

  @action(detail=False, methods=['post'])
  def translate(self, request):
    try:
          image = Image.open(request.data['image'])  # 使用 PIL 打開圖片
          # 進行辨識圖片中的文字
          ocr_text = pytesseract.image_to_string(
              image,
              lang='kor+jpn+eng+chi_tra+chi_sim+fra+deu+spa+ita+rus+por+ara+hin+tha+vie',
          )
          ocr_text = ocr_text.replace('\n', ' ')   # 拿掉換行符號
          ocr_text = ocr_text.replace('. ', '.\n') # 遇到 . 換行

          # 使用 OpenAI API 進行翻譯
          # openai.api_key = settings.OPENAI_API_KEY  # 從 settings 模塊中獲取 API 密鑰
          # response = openai.Completion.create(
          #       engine="text-davinci-003",
          #       prompt=ocr_text,
          #       max_tokens=1000
          #   )
          # openai_text = response.choices[0].text.strip()

          return Response({'data': ocr_text}, status=status.HTTP_200_OK)
          # return Response({'data': openai_text}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

  # 新增，對應前端的 POST 請求
  def create(self, request, *args, **kwargs):
      try:
          # 將前端資料，交給序列化器處理，這三行是標準做法
          serializer = UploadImageSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()

          return Response({'message': '新增成功'}, status=status.HTTP_201_CREATED)
      except Exception as e:
          return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

  # 更新，對應前端的 PUT 請求
  def update(self, request, *args, **kwargs):
    try:
      upload_image = UploadImage.objects.get(id=kwargs.get('pk'))
      serializer = UploadImageSerializer(upload_image, data=request.data, partial=True)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response({ 'message': '更新成功'}, status = status.HTTP_200_OK)
    except UploadImage.DoesNotExist:
      return Response({ 'message': '未找到對應的記錄'}, status = status.HTTP_404_NOT_FOUND)
    except Exception as e:
      return Response({ 'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

  # 刪除，對應前端的 DELETE 請求
  def destroy(self, request, *args, **kwargs):
    try:
      upload_image = UploadImage.objects.get(id=kwargs.get('pk'))
      upload_image.delete()
      return Response({'message':'刪除成功'}, status = status.HTTP_200_OK)
    except UploadImage.DoesNotExist:
      return Response({'message':'未找到對應的紀錄'},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
      return Response({'message':str(e)},status=status.HTTP_400_BAD_REQUEST)

  # 查詢，對應前端的 GET 請求
  def list(self, request):
    upload_images = UploadImage.objects.all()
    serializer = UploadImageSerializer(upload_images, many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)
