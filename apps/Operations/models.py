from django.db import models
from Exams.models import CourseList,Question,PaperList,Paper
from Users.models import UserProfile
from datetime import datetime


class Create_Paper(models.Model):#自定义随机考试
    course = models.ForeignKey(CourseList, verbose_name=u"所属课程", default=1,on_delete=models.CASCADE)
    paper_name = models.ForeignKey(PaperList, verbose_name=u"试卷名称",on_delete=models.CASCADE)
    sin_choice_num = models.IntegerField(verbose_name=u"单选题数", default=1)
    sin_choice_sco = models.IntegerField(verbose_name=u"单选分值", default=1)
    mul_choice_num = models.IntegerField(verbose_name=u"多选题数", default=2)
    mul_choice_sco = models.IntegerField(verbose_name=u"多选分值", default=2)
    jud_num = models.IntegerField(verbose_name=u"判断题数", default=1)
    jud_sco = models.IntegerField(verbose_name=u"判断分值", default=1)
    sho_num = models.IntegerField(verbose_name=u"简答题数", default=1)
    sho_sco = models.IntegerField(verbose_name=u"简答分值", default=10)
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"试题列表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return u"{0}".format(self.paper_name)


class PaperCache(models.Model):#随机考试题目存储位置
    question = models.IntegerField(verbose_name=u"题目")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")
    user = models.ForeignKey(UserProfile, verbose_name=u"用户",on_delete=models.CASCADE)
    class Meta:
        verbose_name = u"试题临时列表"
        verbose_name_plural = verbose_name


# class UserScore(models.Model):#用户试卷对应的成绩
#     user = models.ForeignKey(UserProfile, verbose_name=u"用户",on_delete=models.CASCADE)
#     paper = models.ForeignKey(PaperList, verbose_name=u"试卷",on_delete=models.CASCADE)
#     score = models.IntegerField(verbose_name=u"总分", default=0)
#     add_time = models.DateField(verbose_name=u"录入时间",default=datetime.now)
#
#     class Meta:
#         verbose_name = u"用户总分"
#         verbose_name_plural = verbose_name
#
#     def __unicode__(self):
#         return "{0}({1}) 试卷:{2} | 总分:{3}".format(self.user.nick_name, self.user.id, self.paper.name, self.score)


class UserAnswerLog(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户",on_delete=models.CASCADE)
    course = models.ForeignKey(CourseList, verbose_name=u"课程",on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper,verbose_name=u"试卷",on_delete=models.CASCADE)
    answer = models.TextField(verbose_name=u"用户答案")
    score = models.IntegerField(verbose_name=u"得分")
    add_time = models.DateField(default=datetime.now, verbose_name=u"作答时间")

    class Meta:
        verbose_name = u"用户做题记录"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{0}({1}) score={2}".format(self.user.nick_name,self.user.id,self.score)


class UserCollection(models.Model):#刷题模式下收藏了哪些题目
    user = models.ForeignKey(UserProfile, verbose_name=u"用户",on_delete=models.CASCADE)
    course = models.ForeignKey(CourseList, verbose_name=u"课程",on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name=u"题目",on_delete=models.CASCADE)
    add_time = models.DateField(verbose_name=u"录入时间",default=datetime.now)


class UserRecord(models.Model):#刷题模式下记录到哪一个题目
    user = models.ForeignKey(UserProfile, verbose_name=u"用户",on_delete=models.CASCADE)
    course = models.ForeignKey(CourseList, verbose_name=u"课程",on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name=u"题目",on_delete=models.CASCADE)
    add_time = models.DateField(verbose_name=u"录入时间",default=datetime.now)