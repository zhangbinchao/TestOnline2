from django.shortcuts import render
from django.views.generic.base import View
from .models import PaperList,Question,Paper
from Users.models import UserProfile
from Operations.models import UserAnswerLog,PaperCache,UserRecord
from datetime import datetime
import random
# Create your views here.
class PaperListView(View):
    """试题列表页面"""

    def get(self, request):
        papers = PaperList.objects.filter(is_allow=True)
        # for i in papers:
            # print (i.name, '**', i.id)
        return render(request, "paperlist.html", {"papers": papers, "title": u"试题列表页面"})

class PaperView(View):
    """试卷页"""
    def get(self, request, paper_id):
        if request.user.is_authenticated:
            papers_list = PaperList.objects.filter(id=paper_id)
            for papers_list in papers_list:
                papers_list = papers_list
            single_choice_score1 = papers_list.single_choice_num*papers_list.single_choice_score
            judgment_score1 = papers_list.judgment*papers_list.judgment_score
            multiple_choice_score1 = papers_list.multiple_choice_num*papers_list.multiple_choice_score
            #随机试卷
            if papers_list.random_paper == 1:
                question_list = []
                xz_num = Question.objects.filter(questionType ='xz').count()
                pd_num = Question.objects.filter(questionType = 'pd').count()
                mxz_num = Question.objects.filter(questionType = 'mxz').count()
                seq1 = [i for i in range(1, xz_num)]
                seq2 = [i for i in range(xz_num, xz_num+pd_num)]
                seq3 = [i for i in range(xz_num+pd_num, xz_num+pd_num+mxz_num)]
                question_id_list1 = random.sample(seq1, papers_list.single_choice_num)
                question_id_list2 = random.sample(seq2, papers_list.judgment)
                question_id_list3 = random.sample(seq3, papers_list.multiple_choice_num)
                question_id_list1.extend(question_id_list2)
                question_id_list1.extend(question_id_list3)
                print(question_id_list1)
                for question_id in question_id_list1:
                    question = Question.objects.get(id=question_id)
                    question_list.append(question)
                    Paper_Cache = PaperCache()
                    Paper_Cache.question = question_id
                    Paper_Cache.user = request.user
                    Paper_Cache.add_time = datetime.now()
                    Paper_Cache.save()
                print('get 方法里用户获取的题目编号为', question_id_list1)  # 显示当前题目编号列表
                question_now = tuple(question_list)  # 题目元组
                return render(request, "paper.html", {"question": question_now,"papers_list":papers_list,
                                                      "single_choice_score":single_choice_score1, "judgment_score":judgment_score1,"multiple_choice_score":multiple_choice_score1,
                                                      }
                                                      )
            #固定试卷
            else:
                questions_all = Paper.objects.filter(paper_name_id=paper_id)  # 找到所有试题
                question_list = []
                question_id_list = []
                for questions_ in questions_all:
                    print('paper is ', questions_)
                    question = Question.objects.get(pk=questions_.question_id)
                    question_list.append(question)
                    question_id_list.append(question.id)
                print('get 方法里用户获取的题目编号为', question_id_list)  # 显示当前题目编号列表
                question_now = tuple(question_list)  # 题目元组
                return render(request, "paper.html", {"question": question_now,"papers_list":papers_list,
                                                      "single_choice_score":single_choice_score1, "judgment_score":judgment_score1,"multiple_choice_score":multiple_choice_score1,
                                                      }
                                                      )
        else:
            return render(request, "login.html", {"msg": u'为保证考试客观公正，考题不对未登录用户开放'})

    def post(self, request, paper_id):
        papers_list = PaperList.objects.filter(id=paper_id)
        for papers_list in papers_list:
            papers_list = papers_list
        #随机试卷
        if papers_list.random_paper == 1:
            question_id_lists = PaperCache.objects.filter(user=request.user)
            question_id_list = []
            for question_id in question_id_lists:
                question = Question.objects.get(pk=question_id.question)
                question_id_list.append(question.id)
            title = papers_list.name
            # 分数记录
            user_score = UserAnswerLog()
            # 记录用户
            user_score.user = request.user
            # 记录做题时间
            user_score.add_time = datetime.now()
            temp_score = 0
            user_score.paper_id = papers_list.id
            user_score.course_id = papers_list.course_id
            wrong_question = []
            for i in question_id_list:
                # 根据编号找到用户提交的对应题号的答案
                user_ans = request.POST.get(str(i), "")
                print(u'试题', i, u'收到的答案是', user_ans)
                # 获取题号为 i 的题目元组对象
                temp_question = Question.objects.get(pk=i)
                # 把正确答案与提交的答案比较
                if temp_question.questionType == 'xz':
                    if temp_question.answer == user_ans:
                        temp_score += papers_list.single_choice_score
                        print("试题", temp_question.id, "答案正确")
                    else:
                        question = Question.objects.get(pk=i)
                        wrong_question.append(question)
                elif temp_question.questionType == 'pd':
                    if temp_question.answer == user_ans:
                        temp_score += papers_list.judgment_score
                        print("试题", temp_question.id, "答案正确")
                    else:
                        question = Question.objects.get(pk=i)
                        wrong_question.append(question)
                else:
                    a = str(i) + '_1'
                    b = str(i) + '_2'
                    c = str(i) + '_3'
                    d = str(i) + '_4'
                    e = str(i) + '_5'
                    f = str(i) + '_6'
                    user_ans1 = request.POST.get(a, "")  # 找对应题号的答案
                    user_ans2 = request.POST.get(b, "")  # 找对应题号的答案
                    user_ans3 = request.POST.get(c, "")  # 找对应题号的答案
                    user_ans4 = request.POST.get(d, "")  # 找对应题号的答案
                    user_ans5 = request.POST.get(e, "")  # 找对应题号的答案
                    user_ans6 = request.POST.get(f, "")  # 找对应题号的答案
                    user_ans = user_ans1 + user_ans2 + user_ans3 + user_ans4 + user_ans5 + user_ans6
                    if temp_question.answer == user_ans:
                        temp_score += papers_list.multiple_choice_score
                        print("试题", temp_question.id, "答案正确")
                    else:
                        question = Question.objects.get(pk=i)
                        wrong_question.append(question)
            wrong_question_now = tuple(wrong_question)
            wrong_question_count = len(wrong_question_now)
            user_score.score = temp_score
            user_score.save()
            question_id_lists.delete()
            return render(request, "score.html",
                          {"score": user_score.score, "title": title, "wrong_question": wrong_question_now,
                           "wrong_question_count": wrong_question_count})
        #固定试卷
        else:
            papers = Paper.objects.filter(paper_name_id=paper_id)  # 找到所有试题
            question_id_list = []
            for paper in papers:
                print('paper is ', paper)
                question = Question.objects.get(pk=paper.question_id)
                question_id_list.append(question.id)
            # 找到该用户所有的做题记录
            user_info = UserProfile.objects.get(username=request.user)

            title = paper.paper_name.name
            # 分数记录
            user_score = UserAnswerLog()
            # 记录用户
            user_score.user_id = request.user.id
            # 记录做题时间
            user_score.add_time = datetime.now()
            temp_score = 0
            user_score.paper_id = papers_list.id
            user_score.course_id = papers_list.course_id
            wrong_question = []
            for i in question_id_list:
                # 根据编号找到用户提交的对应题号的答案
                user_ans = request.POST.get(str(i), "")
                print(u'试题', i, u'收到的答案是', user_ans)
                # 获取题号为 i 的题目元组对象
                temp_question = Question.objects.get(pk=i)
                # 把正确答案与提交的答案比较
                if temp_question.questionType == 'xz':
                    if temp_question.answer == user_ans:
                        temp_score += papers_list.single_choice_score
                        print("试题", temp_question.id, "答案正确")
                    else:
                        question = Question.objects.get(pk=i)
                        wrong_question.append(question)
                elif temp_question.questionType == 'pd':
                    if temp_question.answer == user_ans:
                        temp_score += papers_list.judgment_score
                        print("试题", temp_question.id, "答案正确")
                    else:
                        question = Question.objects.get(pk=i)
                        wrong_question.append(question)
                else:
                    a = str(i) + '_1'
                    b = str(i) + '_2'
                    c = str(i) + '_3'
                    d = str(i) + '_4'
                    e = str(i) + '_5'
                    f = str(i) + '_6'
                    user_ans1 = request.POST.get(a, "")  # 找对应题号的答案
                    user_ans2 = request.POST.get(b, "")  # 找对应题号的答案
                    user_ans3 = request.POST.get(c, "")  # 找对应题号的答案
                    user_ans4 = request.POST.get(d, "")  # 找对应题号的答案
                    user_ans5 = request.POST.get(e, "")  # 找对应题号的答案
                    user_ans6 = request.POST.get(f, "")  # 找对应题号的答案
                    user_ans = user_ans1 + user_ans2 + user_ans3 + user_ans4 + user_ans5 + user_ans6
                    if temp_question.answer == user_ans:
                        temp_score += papers_list.multiple_choice_score
                        print("试题", temp_question.id, "答案正确")
                    else:
                        question = Question.objects.get(pk=i)
                        wrong_question.append(question)
            wrong_question_now = tuple(wrong_question)
            wrong_question_count = len(wrong_question_now)
            user_score.score = temp_score
            user_score.save()
            return render(request, "score.html",
                          {"score": user_score.score, "title": title, "wrong_question": wrong_question_now,
                           "wrong_question_count": wrong_question_count})


class TrainView(View):
    """训练模式"""
    def get(self, request,question_id):
        flag1 = 0
        flag2 = 0
        question_now = Question.objects.filter(id=question_id)
        for question_now in question_now:
            question_now = question_now
        question_id = int(question_id)
        question_count = Question.objects.count()
        pre_question_id = question_id-1
        next_question_id = question_id + 1
        return render(request, "train.html", {"question_now": question_now,"pre_question_id": pre_question_id,"next_question_id": next_question_id,
                                              "question_count":question_count,"flag1":flag1,"flag2":flag2,})

    def post(self, request, question_id):
        flag1 = 1
        question_now = Question.objects.filter(id=question_id)
        for question_now in question_now:
            question_now = question_now
        question_id = int(question_id)
        question_count = Question.objects.count()
        pre_question_id = question_id-1
        next_question_id = question_id + 1
        user_ans = request.POST.get(str(question_id), "")
        print(u'试题', user_ans, u'收到的答案是', user_ans)
        if question_now.questionType == 'xz':
            if question_now.answer == user_ans:
                flag2 = 1
                return render(request, "train.html", {"question_now": question_now, "pre_question_id": pre_question_id,
                                                  "next_question_id": next_question_id,
                                                  "question_count": question_count, "flag1": flag1, "flag2": flag2, })
            else:
                flag2 = 0
                return render(request, "train.html", {"question_now": question_now, "pre_question_id": pre_question_id,
                                                  "next_question_id": next_question_id,
                                                  "question_count": question_count, "flag1": flag1, "flag2": flag2, })

        elif question_now.questionType == 'pd':
            if question_now.answer == user_ans:
                flag2 = 1
                return render(request, "train.html", {"question_now": question_now, "pre_question_id": pre_question_id,
                                                  "next_question_id": next_question_id,
                                                  "question_count": question_count, "flag1": flag1, "flag2": flag2, })
            else:
                flag2 = 0
                return render(request, "train.html", {"question_now": question_now, "pre_question_id": pre_question_id,
                                                  "next_question_id": next_question_id,
                                                  "question_count": question_count, "flag1": flag1, "flag2": flag2, })
        else:
            a = str(question_id) + '_1'
            b = str(question_id) + '_2'
            c = str(question_id) + '_3'
            d = str(question_id) + '_4'
            e = str(question_id) + '_5'
            f = str(question_id) + '_6'
            user_ans1 = request.POST.get(a, "")  # 找对应题号的答案
            user_ans2 = request.POST.get(b, "")  # 找对应题号的答案
            user_ans3 = request.POST.get(c, "")  # 找对应题号的答案
            user_ans4 = request.POST.get(d, "")  # 找对应题号的答案
            user_ans5 = request.POST.get(e, "")  # 找对应题号的答案
            user_ans6 = request.POST.get(f, "")  # 找对应题号的答案
            user_ans = user_ans1 + user_ans2 + user_ans3 + user_ans4 + user_ans5 + user_ans6
            if question_now.answer == user_ans:
                flag2 = 1
                return render(request, "train.html", {"question_now": question_now, "pre_question_id": pre_question_id,
                                                  "next_question_id": next_question_id,
                                                  "question_count": question_count, "flag1": flag1, "flag2": flag2, })
            else:
                flag2 = 0
                return render(request, "train.html", {"question_now": question_now, "pre_question_id": pre_question_id,
                                                  "next_question_id": next_question_id,
                                                  "question_count": question_count, "flag1": flag1, "flag2": flag2, })



from django.http import HttpResponseRedirect
from django.urls import reverse

def Quit_Train(request,question_id):
    """退出训练"""
    question_now = Question.objects.filter(id=question_id)
    for question_now in question_now:
        question_now = question_now
    try:
        UserRecord_now = UserRecord.objects.get( user_id=request.user.id,course_id =question_now.course_id )
        UserRecord_now.question_id = question_id
        UserRecord_now.save()
    except:
        UserRecord_now = UserRecord()
        UserRecord_now.add_time = datetime.now()
        UserRecord_now.course_id = question_now.course_id
        UserRecord_now.question_id = question_id
        UserRecord_now.user_id = request.user.id
        UserRecord_now.save()
    question_record = Question.objects.filter(id=question_id)
    return HttpResponseRedirect(reverse('index'))
