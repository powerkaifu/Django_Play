from django.http import Http404, HttpResponse
# django.shortcuts 用於簡化代碼，可以減少 try...except... 的使用，降低耦合，建議使用 django.shortcuts
# 渲染模板用 render 函數
from django.shortcuts import render, get_object_or_404
from .models import Question

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


def results(request, question_id):
  response = "You're looking at the results of question %s."
  return HttpResponse(response % question_id)


def vote(request, question_id):
  return HttpResponse("You're voting on question %s." % question_id)
