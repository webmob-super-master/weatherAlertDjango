from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^alert/(?P<region>\w+)', views.alert, name='alert'),
    url(r'^(?i)ATriggerVerify.txt$', views.file, name='triggerverify'),
]