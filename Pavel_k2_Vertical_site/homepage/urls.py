from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    re_path(r'^booking/(?P<city_from>[^/]+)---(?P<city_to>[^/]+)/$', views.form, name='form'),
    path("rules/", views.rules, name="rules"),
]