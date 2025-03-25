from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("form/", views.form, name="form"),
    path("total_price/", views.total_price, name="total_price"),
]