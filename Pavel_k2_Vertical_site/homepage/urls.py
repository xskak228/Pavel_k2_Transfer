from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    re_path(r'^booking/(?P<city_from>[\w-]+)?---(?P<city_to>[\w-]+)?/$', views.form, name='form'),
    path("total_price/<int:booking_id>/", views.total_price, name="total_price"),
    path("rules/", views.rules, name="rules"),
]