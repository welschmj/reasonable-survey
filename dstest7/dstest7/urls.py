"""
Definition of urls for dstest7.
"""

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:

    # ex: /polls/5/
    url(r'^(?P<question_id>[0-9]+)/$', app.views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', app.views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/(?P<ans_id>[0-9]+)$', app.views.vote, name='vote'),

    url(r'^$', app.views.home, name='home'),
    url(r'^poll/$', app.views.home, name='home'),

    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^summary', app.views.summary, name='summary'),

    # ex: /summary/1
    url(r'^summary/(?P<sid>[0-9]+)', app.views.survey_summary),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include(django.contrib.admindocs.urls)),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Registration URLs
    url('^register/', CreateView.as_view(
            template_name='app/register.html',
            form_class=UserCreationForm,
            success_url='/')),
    # url('^accounts/', include('django.contrib.auth.urls')),
]
