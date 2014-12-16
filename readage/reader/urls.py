from django.conf.urls import patterns, url

from reader import views

urlpatterns = patterns('',
    url(r'(\d+)/$', views.reader, name='reader'),
)


