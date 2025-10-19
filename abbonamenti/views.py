from django.shortcuts import render
from django.http import HttpResponse
from clienti.models import Abbonamento

def index(request):
    abbonamenti = Abbonamento.objects.all().order_by('nAbb')
    abbonamenti_data = []
    for abbonamento in abbonamenti:
        abbonamenti_data.append({
            "nAbb": abbonamento.nAbb,
            "cliente": abbonamento.cliente,
            "inizio": abbonamento.inizio,
            "fine": abbonamento.fine,
            "prezzo": abbonamento.prezzo,
        })
    return render(request, "abbonamenti/abbonamenti.html", {"abbonamenti_data": abbonamenti_data})