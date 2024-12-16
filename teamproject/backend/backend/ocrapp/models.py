from django.db import models

# Create your models here.


class UploadImage(models.Model):
  title = models.TextField(max_length = 100, default = '')           # 標題
  translated_content = models.TextField(default = '')                # 翻譯後的內容
  image = models.ImageField(upload_to = 'images/')                   # 指定上傳的路徑
  created_at = models.DateTimeField(auto_now_add = True)             # 自動添加當前時間

  def __str__(self):
    return self.title
