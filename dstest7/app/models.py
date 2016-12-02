"""
Definition of models.
"""

from django.db import models

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    survey_id = models.ForeignKey('Survey')
    desc_text = models.TextField(default='Answer the question')
    pub_date = models.DateTimeField('date published')
    next_qid = models.ForeignKey('self',null = True, blank=True)
    def __str__(self):
        return self.question_text
   
class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    next_qid = models.ForeignKey(Question, null = True, related_name="question_branch", on_delete=models.SET_NULL, blank=True)
    def __str__(self):
        return self.choice_text

class Survey(models.Model):
    survey_name = models.TextField()
    first_qid = models.ForeignKey(Question,null = True,blank=True)
    def __str__(self):
        return self.survey_name

class Response(models.Model):
    surveyid = models.TextField()
    qid = models.TextField()
    user = models.TextField()
    res = models.TextField()

    class Meta:
        unique_together = ('surveyid', 'user')