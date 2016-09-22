"""
Definition of views.
"""

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from .models import Question, Choice

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'app/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id, ans_id):
    question = get_object_or_404(Question, pk=question_id)
    choice = question.choice_set.get(pk=ans_id)
    choice.votes = choice.votes + 1
    choice.save()
    return detail(request, question_id)

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
            'title':'Home Page',
            'year':datetime.now().year,
            'latest_question_list': latest_question_list
            }
    return render(
        request,
        'app/index.html',
        context
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
