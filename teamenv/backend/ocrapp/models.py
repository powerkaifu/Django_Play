from django.db import models

# Create your models here.


class UploadImage(models.Model):
  category = models.CharField(max_length = 100, default = '')
  edit_content = models.TextField(default = '')
  ai_content = models.TextField(default = '')
  image = models.ImageField(upload_to = 'images/')  # upload_to: 指定上傳的路徑
  created_at = models.DateTimeField(auto_now_add = True)

  def __str__(self):
    return self.category
