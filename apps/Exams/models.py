from django.db import models
from datetime import datetime
from Users.models import UserProfile
# Create your models here.


class CourseList(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"科目名", default="")
    decs = models.CharField(max_length=500, verbose_name=u"科目说明", default="")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:#模型的元数据，指的是“除了字段外的所有内容”，例如排序方式、数据库表名、人类可读的单数或者复数名等等。
        verbose_name = u"考试科目"  #模型数据名称
        verbose_name_plural = verbose_name   #复数名称

    def __unicode__(self):#为了输出是调用比较方便
        return self.name


class Question(models.Model):
    course = models.ForeignKey(CourseList, verbose_name=u"考试科目",on_delete=models.CASCADE)
    questionType = models.CharField(max_length=20, choices=(("single_choice", u"选择题"), ("judgment", u"判断题"), ("multiple_choice", u"多选题"), ("short_answer", u"简答题")), default="single_choice", verbose_name=u"题目类型")
    content = models.TextField(verbose_name=u"题目内容")
    answer = models.TextField(verbose_name=u"正确答案")
    choice_a = models.TextField(verbose_name=u"A选项", default="A.")
    choice_b = models.TextField(verbose_name=u"B选项", default="B.")
    choice_c = models.TextField(verbose_name=u"C选项", default="C.")
    choice_d = models.TextField(verbose_name=u"D选项", default="D.")
    choice_e = models.TextField(verbose_name=u"E选项", default="E.")
    choice_f = models.TextField(verbose_name=u"F选项", default="F.")
    note = models.TextField(verbose_name=u"备注信息", default= u"问答题在此处做答")
    boolt = models.TextField(verbose_name=u"判断正误正确选项", default= "对")
    boolf = models.TextField(verbose_name=u"判断正误错误选项", default= "错")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")
    choice_num = models.IntegerField(verbose_name=u"选项数", default=4)

    class Meta:
        verbose_name = u"题库"
        verbose_name_plural = verbose_name

    def get_content_display(self, field):
        return self.content

    def __unicode__(self):
        model = Question
        return "{0}(题干:{1} | 正确答案:{2} )".format(self.course.name, self.content, self.answer)



class PaperList(models.Model):#用于查看往期考试题目可能不用
    course = models.ForeignKey(CourseList, verbose_name=u"所属课程",on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"试卷名", default=u"")
    is_allow = models.BooleanField(default=False, verbose_name=u"启用随机组卷")
    add_time = models.DateField(default=datetime.now, verbose_name=u"开考时间")
    single_choice_num = models.IntegerField(verbose_name=u"单选题数", default=0)
    single_choice_score = models.IntegerField(verbose_name=u"单选分值", default=0)
    judgment = models.IntegerField(verbose_name=u"判断题数", default=0)
    judgment_score = models.IntegerField(verbose_name=u"判断分值", default=0)
    multiple_choice_num = models.IntegerField(verbose_name=u"多选题数", default=0)
    multiple_choice_score = models.IntegerField(verbose_name=u"多选分值", default=0)
    random_paper = models.BooleanField(default=True, verbose_name=u"随机卷")

    class Meta:
        verbose_name = u"试卷列表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return u"{0}(试卷名称:{1} | 使用状态:{2})".format(self.course.name, self.name, self.is_allow)


class Paper(models.Model):#题目如何存储
    course = models.ForeignKey(CourseList, verbose_name=u"所属课程", default=1,on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name=u"题目",on_delete=models.CASCADE)
    paper_name = models.ForeignKey(PaperList, verbose_name=u"试卷名称",on_delete=models.CASCADE)
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")
    score = models.IntegerField(verbose_name=u"分值", default=0)

    class Meta:
        verbose_name = u"试题列表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return u"{0} ({1})".format(self.paper_name, self.question.content)