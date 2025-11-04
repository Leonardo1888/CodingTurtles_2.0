from django.urls import path
from . import views

#aggiunto sala/ o cliente/ all'inizio url per distinguere
urlpatterns = [
    path("sala/<str:codice_sala>/", views.prenotazioni_sala, name="prenotazioni_sala"),    #collegamento con sale
    path("cliente/<str:codice_cliente>/", views.prenotazioni_cliente, name="prenotazioni_cliente"),    #collegamento con clienti
]