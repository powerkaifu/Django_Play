from django.http import Http404, HttpResponse, HttpResponseRedirect
# django.shortcuts 用於簡化代碼，可以減少 try...except... 的使用，降低耦合，建議使用 django.shortcuts
# 渲染模板用 render 函數
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F
from django.views import generic  # 用於簡化視圖的代碼

# 引入模型
from .models import Question, Choice

# Create your views here.


def index(request):
  latest_question_list = Question.objects.order_by('-pub_date')[: 5]
  context = {
      "latest_question_list": latest_question_list,
  }  # 上下文
  return render(request, "polls/index.html", context)  # 渲染模板


# def detail(request, question_id):
#   try:
#     question = Question.objects.get(pk = question_id)  # pk 是主鍵的縮寫，固定用法
#   except Question.DoesNotExist:
#     raise Http404("Question does not exist")
#   return render(request, "polls/detail.html", { "question": question})


# 常用，也可以使用 get_object_or_404() 函數來簡化以上的代碼
def detail(request, question_id):
  question = get_object_or_404(Question, pk = question_id)
  context = {
      "question": question,
  }
  return render(request, "polls/detail.html", context)


def vote(request, question_id):
  question = get_object_or_404(Question, pk = question_id)  # 從取得問題開始
  try:
    selected_choice = question.choice_set.get(pk = request.POST['choice'])  # 反向選取取得選擇的選項
  except ( KeyError, Choice.DoesNotExist ):
    context = {
        "question": question,
        "error_message": "You didn't select a choice.",  # 用於前端顯示錯誤訊息
    }
    return render(request, "polls/detail.html", context)
  else:
    selected_choice.votes = F('votes') + 1  # 可以避免資源競爭，避免使用者同時投票造成不一致
    selected_choice.save()  # 保存選項
    return HttpResponseRedirect(reverse('polls:results', args = (question.id,)))  # 重新導向到 results 頁面


def results(request, question_id):
  question = get_object_or_404(Question, pk = question_id)
  context = { "question": question}
  return render(request, "polls/results.html", context)


# 以下為對應的改良後的路由 ------------------------------------------------------------
## https://docs.djangoproject.com/zh-hans/5.1/intro/tutorial04/#amend-urlconf
class IndexView(generic.ListView):
  template_name = "polls/index.html"
  context_object_name = "latest_question_list"

  def get_queryset(self):
    return Question.objects.order_by('-pub_date')[: 5]


class DetailView(generic.DetailView):
  model = Question
  template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
  model = Question
  template_name = "polls/results.html"
