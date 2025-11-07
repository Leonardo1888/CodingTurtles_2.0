from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.sale_create, name="sale_create"),
    path("update/", views.sale_update, name="sale_update"),
    path("delete/", views.sale_delete, name="sale_delete"),
]