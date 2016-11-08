"""
Definition of views.
"""

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from graphos.sources.model import ModelDataSource
from graphos.renderers import gchart
from .models import Question, Choice, Survey

def detail(request, question_id):
    #If the item being passed is a survey, then get the
    #fqid
    try:
        survey = Survey.objects.get(pk=question_id)
        fqid = survey.first_qid.id
    #Otherwise, its a question
    except Survey.DoesNotExist:
        fqid=question_id

    question = get_object_or_404(Question, pk=fqid)
    if request.user.is_authenticated:
        # Example graph that works, but doesn't really make sense yet
        queryset = Choice.objects.filter(question=fqid)
        data_source = ModelDataSource(queryset,
                                      fields=[ 'choice_text', 'votes'])
        chart = gchart.PieChart(data_source, options={'is3D': True, 'pieSliceText':
                            'value'})
    else: chart=""
    return render(request, 'app/detail.html', {'question': question, 'chart':
        chart } )

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id, ans_id):
    question = get_object_or_404(Question, pk=question_id)
    choice = question.choice_set.get(pk=ans_id)
    choice.votes = choice.votes + 1

    # goes to the question if it is defined by choice
    if choice.next_qid:
        next_q = choice.next_qid.id
    # otherwise go to the question defined by question
    elif question.next_qid:
        next_q = question.next_qid.id
    # otherwise go to homepage
    else:
        next_q = ""

    choice.save()
    if next_q:
        return detail(request,next_q)
    else:
        return home(request)

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    latest_question_list = Survey.objects.all()
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
