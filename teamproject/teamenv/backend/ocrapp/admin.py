from django.contrib import admin
from .models import UploadImage

# Register your models here.


class UploadImageAdmin(admin.ModelAdmin):
  list_display = [field.name for field in UploadImage._meta.fields]
  list_filter = ['created_at']
  search_fields = ['image']


admin.site.register(UploadImage, UploadImageAdmin)
