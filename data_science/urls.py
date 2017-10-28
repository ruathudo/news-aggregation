from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<entry_id>[-\w]+)/$', views.related_news, name='related_news'),
]
