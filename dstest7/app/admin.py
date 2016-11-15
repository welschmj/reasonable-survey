from django.contrib import admin
from .models import Question, Choice, Survey,Response

admin.site.register(Question)

admin.site.register(Choice)

admin.site.register(Survey)
admin.site.register(Response)