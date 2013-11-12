from django.conf.urls import patterns, url
from cloto import views

urlpatterns = patterns('',
    (r'^somepage/$', views.some_page),
    url(r'^somepage2/$', views.test),
)
