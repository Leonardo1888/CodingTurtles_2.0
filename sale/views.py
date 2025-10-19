from django.shortcuts import render
from django.http import HttpResponse
from .models import Sala, FasciaOraria, Prenotazione

def index(request):
    sale = Sala.objects.all()
    sale_data = []
    for sala in sale:
        n_fasce = FasciaOraria.objects.filter(sala=sala).count()
        n_prenotazioni = Prenotazione.objects.filter(sala=sala).count()
        sale_data.append({
            "codice": sala.codice,
            "nome": sala.nome,
            "tema": sala.tema,
            "mq": sala.mq,
            "n_fasce": n_fasce,
            "n_prenotazioni": n_prenotazioni,
        })
    return render(request, "sale/sale.html", {"sale_data": sale_data})