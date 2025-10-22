from django.urls import path
from . import views

urlpatterns = [
    path("<str:codice_sala>/", views.prenotazioni, name="prenotazioni"),
]