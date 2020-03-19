from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user=User()
    name=models.CharField('姓名',max_length=32)

    def __str__(self):
        return self.name



# from django.db import models
#
#
# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#
#
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)