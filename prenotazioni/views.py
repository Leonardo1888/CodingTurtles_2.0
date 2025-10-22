from django.shortcuts import render
from sale.models import Prenotazione

def prenotazioni(request, codice_sala):
    prenotazioni = Prenotazione.objects.filter(sala__codice=codice_sala)
    return render(request, "prenotazioni/prenotazioni.html", {'prenotazioni_data': prenotazioni})