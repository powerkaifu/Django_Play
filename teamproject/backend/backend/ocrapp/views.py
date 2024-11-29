# from django.shortcuts import render
# from rest_framework import generics  # 用於繼承API視圖

from .models import UploadImage
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action
from .serializers import uploadSerializer
from PIL import Image
import pytesseract
# import openai

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 指定 Tesseract 執行檔的路徑

# openai.api_key = ''


class ImageUploadViewSet(viewsets.ViewSet):
  parser_classes = ( MultiPartParser, FormParser, JSONParser )  # 設置解析器

  @action(detail=False, methods=['post'])
  def translate(self, request):
    # print(request.data)
    serializer = uploadSerializer(data=request.data)  # 將上傳的圖片資料，交給序列化器處理
    if serializer.is_valid():
        image = Image.open(request.data['image'])  # 使用 PIL 打開圖片
        # 進行辨識圖片中的文字
        ocr_text = pytesseract.image_to_string(
            image,
            lang='kor+jpn+eng+chi_tra+chi_sim',
            # lang='kor+jpn+eng+chi_tra+chi_sim+fra+deu+spa+ita+rus+por+ara+hin+tha+vie',
        )
        ocr_text = ocr_text.replace('\n', ' ')   # 拿掉換行符號
        ocr_text = ocr_text.replace('. ', '.\n') # 遇到 . 換行
        return Response({'data': ocr_text}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  # 新增，對應前端的 POST 請求
  def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = uploadSerializer(data=request.data)  # 將上傳的資料，交給序列化器處理
        if serializer.is_valid():
            upload_image = serializer.save()  # 儲存上傳圖片的圖片路徑，且會回傳一個 UploadImage 實例
            translated_content = request.data.get('translated_content')   # 獲取前端傳來的翻譯後的文字
            title = request.data.get('title')   # 獲取前端傳來的標題
            upload_image.title = title
            upload_image.translated_content = translated_content
            upload_image.save() # 儲存翻譯結果到資料庫

            return Response({'message':'新增成功','data': translated_content, 'id': upload_image.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  # 更新，對應前端的 PUT 請求(這邊前端用 modal 來做)
  def update(self, request, *args, **kwargs):
    try:
      data = request.data.get('data') # 從請求中獲取要更新的內容
      upload_image = UploadImage.objects.get(id = kwargs.get('pk'))
      upload_image.edit_content = data
      upload_image.save()
      return Response({ 'message': '更新成功'}, status = status.HTTP_200_OK)
    except UploadImage.DoesNotExist:
      return Response({ 'message': '未找到對應的記錄'}, status = status.HTTP_404_NOT_FOUND)
    except Exception as e:
      return Response({ 'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

  def list(self, request):
    upload_images = UploadImage.objects.all()
    serializer = uploadSerializer(upload_images, many = True) # 將每一個 UploadImage 實例序列化為 JSON 格式
    return Response(serializer.data, status = status.HTTP_200_OK)

  def destroy(self, request, *args, **kwargs):
    try:
      upload_image = UploadImage.objects.get(id=kwargs.get('pk'))
      upload_image.delete()
      return Response({'message':'刪除成功'}, status=status.HTTP_204_NO_CONTENT)
    except UploadImage.DoesNotExist:
      return Response({'message':'未找到對應的紀錄'},status=status.HTTP_400_NOT_FOUND)
    except Exception as e:
      return Response({'messsage':str(e)},status=status.HTTP_400_BAD_REQUEST)