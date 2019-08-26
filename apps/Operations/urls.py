from django.urls import path,include,re_path
from .views import collect,history,del_collect,enquire_collect

app_name = 'Operations'

urlpatterns = [
    #试卷列表
    path('collect/<question_id>/', collect , name="collect"),
    path('history/', history , name="history"),
    path('enquire_collect/', enquire_collect, name="enquire_collect"),
    path('del_collect/<question_id>/', del_collect, name="del_collect"),

]