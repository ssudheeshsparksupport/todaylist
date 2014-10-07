from django.conf.urls import patterns, url
from today import views
urlpatterns = patterns('',
    url(r'^$', views.signup, name='signup'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^projectadd/$', views.projectadd, name='projectadd'),
    url(r'^taskadd/$', views.taskadd, name='taskadd'),
    url(r'^taskediting/(?P<id>\d+)/$', views.taskediting, name='taskediting'),#(?P<id>) here id is the function parameter
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^taskdeleting/(?P<id>\d+)/$', views.taskdeleting, name='taskdeleting'),
    url(r'^checkboxdeleting/$', views.checkboxdeleting, name='checkboxdeleting'),
    url(r'^projectlist/$', views.projectlist, name='projectlist'),
    url(r'^projectdeleting/(?P<id>\d+)/$', views.projectdeleting, name='projectdeleting'),
    url(r'^projectlistone/$', views.projectlistone, name='projectlistone'),
    url(r'^getconsole/$', views.getconsole, name='getconsole'),
    url(r'^getconsoletasks/$', views.getconsoletasks, name='getconsoletasks'),
)