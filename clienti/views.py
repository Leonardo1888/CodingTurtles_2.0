from django.shortcuts import render
from django.http import HttpResponse
from .models import Cliente, Abbonamento
from sale.models import Prenotazione

def index(request):
    clienti = Cliente.objects.all().order_by('codice')
    clienti_data = []
    for cliente in clienti:
        n_abb = Abbonamento.objects.filter(cliente=cliente).count()
        n_prenotazioni = Prenotazione.objects.filter(cliente=cliente.codice).count()
        clienti_data.append({
            "codice": cliente.codice,
            "nome": cliente.nome,
            "cognome": cliente.cognome,
            "cf": cliente.cf,
            "dataNas": cliente.dataNas,
            "indirizzo": cliente.indirizzo,
            "tel": cliente.tel,
            "email": cliente.email,
            "n_abb": n_abb,
            "n_prenotazioni": n_prenotazioni,
        })
    return render(request, "clienti/clienti.html", {"clienti_data": clienti_data})