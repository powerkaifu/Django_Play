from django.db import models

# Create your models here.


class UploadImage(models.Model):
  title = models.TextField(max_length = 100, default = '未填入標題')
  translated_content = models.TextField(default = '')
  image = models.ImageField(upload_to = 'images/')  # upload_to: 指定上傳的路徑
  created_at = models.DateTimeField(auto_now_add = True)

  def __str__(self):
    return self.title
