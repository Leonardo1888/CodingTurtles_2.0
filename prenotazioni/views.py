from django.shortcuts import render
from sale.models import Prenotazione 
from clienti.models import Abbonamento
from django.db.models import Q
import re

def index(request):
    prenotazioni = Prenotazione.objects.all().order_by('data', 'ora')
    
    # Recupera i parametri di filtro dalla richiesta GET
    cliente = request.GET.get('cliente', '').strip()
    sala = request.GET.get('sala', '').strip()
    data_min = request.GET.get('inizio_prenotazione_min', '').strip()
    data_max = request.GET.get('inizio_prenotazione_max', '').strip()
    ora_min = request.GET.get('ora_prenotazione_min', '').strip()
    ora_max = request.GET.get('ora_prenotazione_max', '').strip()
    posto = request.GET.get('posto', '').strip()
    abbonamento = request.GET.get('abbonamento', '').strip()

    # Applica i filtri al queryset
    if cliente:
        prenotazioni = prenotazioni.filter(cliente__icontains=cliente)
    if sala:
        prenotazioni = prenotazioni.filter(sala__codice__icontains=sala)
    if data_min:
        prenotazioni = prenotazioni.filter(data__gte=data_min)
    if data_max:
        prenotazioni = prenotazioni.filter(data__lte=data_max)
    if ora_min:
        prenotazioni = prenotazioni.filter(ora__gte=ora_min)
    if ora_max:
        prenotazioni = prenotazioni.filter(ora__lte=ora_max)
    if posto:
        if posto.isdigit():
            prenotazioni = prenotazioni.filter(posto=int(posto))
    if abbonamento:
        prenotazioni = prenotazioni.filter(abbonamento__icontains=abbonamento)

    # Costruzione dati per il template
    prenotazioni_data = []
    for p in prenotazioni:
        # Estrae codice sala dal formato "(S022) - Nome Sala"
        match = re.search(r'\(([^)]+)\)', str(p.sala))
        codice_sala = match.group(1) if match else ''

        prenotazioni_data.append({
            "cliente": f"{p.cliente.nome} {p.cliente.cognome}",
            "codice_cliente": p.cliente.codice,
            "sala": p.sala, 
            "codice_sala": codice_sala,
            "data": p.data,
            "ora": p.ora,
            "posto": p.posto,
            "abbonamento": p.abbonamento, 
        })

    # Dizionario dei filtri per repopolare il form nel template
    filters = {
        'cliente': cliente,
        'sala': sala,
        'inizio_prenotazione_min': data_min,
        'inizio_prenotazione_max': data_max,
        'ora_prenotazione_min': ora_min,
        'ora_prenotazione_max': ora_max,
        'posto': posto,
        'abbonamento': abbonamento,
    }

    # Renderizza la pagina
    return render(request, "prenotazioni/prenotazioni.html", {
        "prenotazioni_data": prenotazioni_data,
        "filters": filters,
    })