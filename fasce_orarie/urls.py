from django.urls import path
from . import views

app_name = "fasce_orarie" 

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:codice_sala>/', views.index, name='index'),
]