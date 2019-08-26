from django.shortcuts import render,redirect,HttpResponse
from .models import UserCollection,UserAnswerLog
from django.views.generic.base import View
from Exams.models import Question
from Users.models import UserProfile
from datetime import datetime
# Create your views here.

def collect(request,question_id):
    """收藏"""
    questions = Question.objects.filter(id=question_id)
    for question in questions:
        a = question
    if not UserCollection.objects.filter(user=request.user,question_id=question_id):
        User_Collection = UserCollection()
        User_Collection.user_id = request.user.id
        User_Collection.question_id = a.id
        User_Collection.add_time = datetime.now()
        User_Collection.course_id = a.course_id
        User_Collection.save()
        string = '<h3>收藏成功</h3>'
        return HttpResponse(string)
    else:
        string = '<h3>您已经收藏过该题了</h3>'
        return HttpResponse(string)

def enquire_collect(request):
    """查看收藏"""
    if request.user.is_authenticated:
        collections = UserCollection.objects.filter(user_id=request.user.id)
        question_list = []
        for collection in collections:
            a = Question.objects.get(pk=collection.question_id)
            question_list.append(a)
        return render(request, 'collection.html', {"question_list": question_list,})
    else:
        return render(request, "login.html", {"msg": u'为保护用户信息，不对未登录用户开放'})

def del_collect(request,question_id):
    """取消收藏"""
    UserCollection.objects.get(id=question_id,user_id=request.user.id).delete()
    return redirect('/operations/enquire_collect/')


def history(request):
    """历史成绩"""
    if request.user.is_authenticated:
        user_info = UserProfile.objects.get(username=request.user)
        if user_info.identity =='teacher':
            hiss = UserAnswerLog.objects.all()
        else:
            hiss = UserAnswerLog.objects.filter(user=request.user)
        return render(request, 'history.html', locals())
    else:
        return render(request, "login.html", {"msg": u'为保护用户信息，不对未登录用户开放'})


# def paperlist_teacher(request):
#     UserCollection.objects.get(id=question_id,user_id=request.user.id).delete()
#     return redirect('/operations/enquire_collect/')