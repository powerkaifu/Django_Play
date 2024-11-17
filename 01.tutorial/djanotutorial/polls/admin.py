# 設定後台管理的功能
from django.contrib import admin  # 默認的管理員應用
from .models import Question, Choice  # 引入 Question、Choice 模型

# Register your models here.


# 可以設定 Choice 用 inline 方式顯示，另一個方式是 StackedInline(堆疊式)
class ChoiceInline(admin.TabularInline):
  model = Choice
  extra = 0  # 不寫為預設，會多出 3 個選項欄位


# 自訂義後台管理介面
class QuestionAdmin(admin.ModelAdmin):
  list_filter = ["pub_date"]  # 可以設定過濾器
  search_fields = ["question_text"]  # 可以設定搜索欄位
  list_display = [ "question_text", "pub_date", "was_published_recently"]  # 後台要顯示的欄位
  # 可以用 fieldsets 定義字段的分組，這樣可以更好的組織字段
  fieldsets = [
      (
          '日期',
          {
              'fields': ['pub_date'],
              'classes': ['collapse'],  # 可以被折疊
          }
      ),
      ( '描述', {
          'fields': ['question_text'],
      } ),
  ]
  # 可以設定問題與選項的關聯，讓它們在同一頁面顯示，選向會用 inline 方式顯示
  inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)  # 註冊自訂義後台管理介面
admin.site.register(Choice)  # 註冊 Choice 模型
