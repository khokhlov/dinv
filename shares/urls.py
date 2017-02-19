from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^item/(?P<id>[\d]+)/$', views.item, name='share_item'),
]

