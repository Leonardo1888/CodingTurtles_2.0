from django.shortcuts import render
from sale.models import Prenotazione

def prenotazioni_sala(request, codice_sala):     #collegamento con sala
    prenotazioni = Prenotazione.objects.filter(sala__codice=codice_sala)    #sala__codice, si usa __ perché è una foreign key
    return render(request, "prenotazioni/prenotazioni.html", {'prenotazioni_data': prenotazioni})

def prenotazioni_cliente(request, codice_cliente):  #collegamento con cliente
    prenotazioni = Prenotazione.objects.filter(cliente=codice_cliente)
    return render(request, "prenotazioni/prenotazioni.html", {'prenotazioni_data': prenotazioni})