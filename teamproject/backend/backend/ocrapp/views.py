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
  def translate(self, request, *args, **kwargs):
    try:
        # 使用 pillow 打開圖片
        image = Image.open(request.data['image'])

        # 進行辨識圖片中的文字，並設定語言
        ocr_text = pytesseract.image_to_string(
            image,
            # lang='kor+jpn+eng+chi_tra+chi_sim+fra+deu+spa+ita+rus+por+ara+hin+tha+vie',
            lang='kor+jpn+eng+chi_tra+chi_sim',
        )

        ocr_text = ocr_text.replace('\n', ' ')   # 拿掉換行符號
        ocr_text = ocr_text.replace('. ', '.\n') # 遇到 . 換行

        # 使用 OpenAI API 進行翻譯
        openai.api_key = settings.OPENAI_API_KEY  # 從 settings 模塊中獲取 API 密鑰

        # 呼叫 OpenAI API，使用語言學專家的多重身份
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=1000,
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": """
                        你是一位精通多國語言且耐心的語言學專家、電腦科學家，專注於幫助初學者理解語言與電腦科學知識。
                        你的任務是幫助非母語學生理解文本，請按照以下要求進行，如果是非英文的語言，只需做第 1 項即可：
                        1.將每句原文先列出來，再翻譯成中文。
                          <原文句子>
                          <翻譯句子>
                        2.列出常用或困難的單字，提供一個使用該字詞的例句（用英文和中文提供）。
                          例句結束不要加上標點符號
                          常用或困難單字：
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
          serializer = UploadImageSerializer(data=request.data) # 將前端傳入的數據進行序列化，將 JSON 格式轉換為 Python 對象
          serializer.is_valid(raise_exception=True) # 驗證數據是否有效
          serializer.save() # 將數據保存到資料庫
          return Response({'message': '新增成功'}, status=status.HTTP_201_CREATED)
      except Exception as e:
          return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

  # 更新，對應前端的 PUT 請求
  def update(self, request, *args, **kwargs):
    try:
      upload_image = UploadImage.objects.get(id=kwargs.get('pk')) # 前端傳入的 id與資料庫中的 id 進行比對
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
  def list(self, request, *args, **kwargs):
    upload_images = UploadImage.objects.all()
    serializer = UploadImageSerializer(upload_images, many = True) # 序列化並處理多個數據
    return Response(serializer.data, status = status.HTTP_200_OK)
