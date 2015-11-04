from django.conf.urls import url
from . import views

__author__ = 'snake'


urlpatterns = (
    url(r'^m2m/$', views.m2m_ajax, name='m2m_ajax'),
)