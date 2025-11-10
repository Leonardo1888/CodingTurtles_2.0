from django.urls import path
from . import views

app_name = "prenotazioni"  # serve per {% url 'prenotazioni:prenotazioni_sala' %}

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:codice_sala>/', views.index, name='index'),
]
