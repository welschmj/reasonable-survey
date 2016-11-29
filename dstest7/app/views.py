"""
Definition of views.
"""

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from datetime import datetime
from graphos.sources.model import ModelDataSource
from graphos.renderers import gchart
from .models import Question, Choice, Survey, Response

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

def results(request, survey_id):
    assert isinstance(request, HttpRequest)
    # get all responses from model
    user_resp_list = Response.objects.filter(surveyid=survey_id, user=request.user.username)
    survey_name = survey_id.survey_name

    # store the questions and responses
    responses = []
    for chosen in user_resp_list:
        question = Question.objects.get(pk=chosen.qid)
        responses.append((question, chosen.res))
    
    # save in context
    context = {
            'survey_name':survey_name,
            'resp_list':responses
            }
    
    # render the new page
    return render(request, 'app/results.html', context)

def vote(request, question_id, ans_id):
    question = get_object_or_404(Question, pk=question_id)
    choice = question.choice_set.get(pk=ans_id)
    choice.votes = choice.votes + 1
    res = Response.objects.create(surveyid=question.survey_id.pk,qid = question.pk,res = choice.choice_text,user = request.user.username)
    # goes to the question if it is defined by choice
    if choice.next_qid:
        next_q = choice.next_qid.id
    # otherwise go to the question defined by question
    elif question.next_qid:
        next_q = question.next_qid.id
    # otherwise go to homepage
    else:
        next_q = ""

    res.save()
    choice.save()
    if next_q:
        return detail(request,next_q)
    else:
        return results(request, question.survey_id)

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

def summary(request):
    allsurveys = Survey.objects.all()
    graphs = []
    for survey in allsurveys:
        allquestions = Question.objects.all().filter(survey_id=survey.id)
        for question in allquestions:
            choices = Choice.objects.filter(question = question.id)
            data_source = ModelDataSource(choices, fields=['choice_text', 'votes'])
            chart = gchart.PieChart(data_source,
                    options={'is3D': True,
                    'pieSliceText': 'value',
                    'title': question.question_text})
            graphs.append((chart, survey.survey_name))
    return render(request, 'app/summary.html', {'graphs': graphs})

def survey_summary(request, sid):
    allquestions = Question.objects.all().filter(survey_id = sid)
    graphs = []
    survey_name = Survey.objects.get(pk=sid).survey_name
    for question in allquestions:
        choices = Choice.objects.filter(question = question.id)
        data_source = ModelDataSource(choices, fields=['choice_text', 'votes'])
        chart = gchart.PieChart(data_source,
                options={'is3D': True,
                'pieSliceText': 'value',
                'title': question.question_text})
        graphs.append(chart)
    return render(request, 'app/survey_summary.html',
            {   'graphs': graphs,
                'survey_name': survey_name
            })
