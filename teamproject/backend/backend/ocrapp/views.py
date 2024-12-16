# 使用第三方庫
from .models import UploadImage                                               # 導入模型，用於操作資料庫
from django.conf import settings                                              # settings 模塊，用於獲取設置的變數
from rest_framework import viewsets, status                                   # viewsets 和 status 類，用於創建 API 視圖和設置狀態碼
from rest_framework.response import Response                                  # 返回數據給前端
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser    # 解析器，用於解析及驗證前端傳入的數據
from rest_framework.decorators import action                                  # 裝飾器，創建自定義的 action 動作
from rest_framework import serializers                                        # 用來拋出序列化器的異常
from .serializers import UploadImageSerializer                                # 序列化器，用於前後端數據的轉換及驗證
from PIL import Image, ImageOps, ImageFilter                                  # PIL 庫的模組，處理圖片
import pytesseract                                                            # pytesseract 模組，用於辨識圖片中的文字
import openai                                                                 # OpenAI API 模組，用於翻譯文字
import os                                                                     # os 模組，用於刪除圖片

# 指定 Tesseract 執行檔的路徑
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ImageUploadViewSet(viewsets.ViewSet):
  # 設置解析器，用於解析前端傳入的數據，未設置會使用默認的解析器
  parser_classes = ( MultiPartParser, FormParser, JSONParser )

  # 新增自定義的 action 動作，用於圖片翻譯
  @action(detail=False, methods=['post'])
  def translate(self, request, *args, **kwargs):
    try:
        # 使用 pillow 打開圖片
        image = Image.open(request.data['image'])

        # 預處理圖片：轉換為灰階
        gray_image = ImageOps.grayscale(image)

        # 預處理圖片：使用自適應閾值進行二值化
        binary_image = gray_image.filter(ImageFilter.MedianFilter(size=5))
        binary_image = gray_image.point(lambda x: 0 if x < 127 else 255, '1')

        # 進行辨識圖片中的文字，並設定語言
        ocr_text = pytesseract.image_to_string(
            binary_image,
            lang='chi_tra+eng+jpn',                   # 設定語言為繁體中文和英文
            config='--psm 6 --oem 3'                  # 設定辨識模式和引擎
        )

        # 格式化 OCR 文本
        ocr_text = ocr_text.replace('\n', '')       # 拿掉換行符號
        ocr_text = ocr_text.replace('. ', '.\n')    # 遇到 . 換行


        # 使用 OpenAI API 進行翻譯
        openai.api_key = settings.OPENAI_API_KEY    # 從 settings 模塊中獲取 API 密鑰
        # 呼叫 OpenAI API 進行翻譯
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=1500,
            temperature=0.1,
            messages=[
                {
                    "role": "system",
                    "content": """
                        你是一位精通多國語言且耐心的語言學專家、電腦科學專家，
                        專注於幫助初學者理解語言與電腦科學知識。
                        你的任務是幫助台灣學生理解非繁體中文的文本，請按照以下要求進行，

                        1.將每句原文一句列出來，再翻譯成中文，空行後再換下一句，遇到標題也是這樣做。
                          <原文>
                          <翻譯>
                        2.列出 5 個常用或困難的單字，提供一個使用該字詞的例句（用英文和中文提供）。
                          例句結束不要加上標點符號
                          <常用或困難單字>
                          <字詞原文> <中文翻譯>
                          <一個使用該字詞的例句（用英文和中文提供）>
                        3.不需要列出常用或困單字數字編號。
                    """
                },
                {
                    "role": "user",
                    "content": f"\n\n{ocr_text}"
                }
            ]
        )

        openai_text = response['choices'][0]['message']['content']
        return Response({'data': openai_text}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

  # 新增，對應前端的 POST 請求
  def create(self, request, *args, **kwargs):
      try:
         # DRF 使用設置的解析器處理前端傳入的數據
          serializer = UploadImageSerializer(data=request.data)                         # 進行序列化，將 JSON 格式轉換為 Python 對象
          serializer.is_valid(raise_exception=True)                                     # 驗證數據是否有效
          serializer.save()                                                             # 將數據保存到資料庫
          return Response({'message': '新增成功'}, status=status.HTTP_201_CREATED)
      except serializers.ValidationError as e:
          print("Validation Error:", e.detail)
          return Response({'message': e.detail}, status=status.HTTP_400_BAD_REQUEST)

  # 更新，對應前端的 PUT 請求
  def update(self, request, *args, **kwargs):
    try:
      upload_image = UploadImage.objects.get(id=kwargs.get('pk'))                        # 前端傳入的 id 與資料庫中的 id 進行比對
      serializer = UploadImageSerializer(upload_image, data=request.data, partial=True)  # 允許部分自動更新
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

      image_path = upload_image.image.path
      if os.path.exists(image_path):
        os.remove(image_path)

      upload_image.delete()
      return Response({'message':'刪除成功'}, status = status.HTTP_200_OK)
    except UploadImage.DoesNotExist:
      return Response({'message':'未找到對應的紀錄'},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
      return Response({'message':str(e)},status=status.HTTP_400_BAD_REQUEST)

  # 查詢，對應前端的 GET 請求
  def list(self, request, *args, **kwargs):
    upload_images = UploadImage.objects.all()
    serializer = UploadImageSerializer(upload_images, many = True) # 序列化並處理多個數據
    return Response(serializer.data, status = status.HTTP_200_OK)
