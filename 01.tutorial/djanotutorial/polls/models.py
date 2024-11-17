import datetime  # 用於處理日期時間

from django.db import models
from django.contrib import admin
from django.utils import timezone  # 用於處理時區

# Create your models here.


# 模組都是 models.Model 的子類別
class Question(models.Model):
  question_text = models.CharField('question_text(問題描述)', max_length = 200)  # 後台的欄位名稱，易閱讀為主
  pub_date = models.DateTimeField('pub_date(發布日期)')  # 顯示在後台管理介面的名稱

  @admin.display(
      boolean = True,
      ordering = 'pub_date',
      description = 'Published recently?',
  )
  def was_published_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days = 1) <= self.pub_date <= now  # 判斷問題是否是最近發布的

  def __str__(self):
    return self.question_text  # 回傳問題文字，用於後台管理介面，會在列表中顯示，沒有使用會顯示 Question object(1) 這樣的字串


class Choice(models.Model):
  # 每個 Choice 都關聯到一個 Question，一個問題可以有多個選項，但每個選項只能屬於一個問題
  question = models.ForeignKey(Question, on_delete = models.CASCADE)
  choice_text = models.CharField(max_length = 200)
  votes = models.IntegerField(default = 0)

  def __str__(self):
    return self.choice_text
