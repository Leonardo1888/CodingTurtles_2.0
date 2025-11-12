from django.shortcuts import render
from sale.models import FasciaOraria 
from django.db.models import Q
import re


def index(request):
    """Lista delle fasce orarie con filtro via GET.

    Supporta i parametri GET:
      - sala: ricerca parziale (icontains) sul codice della sala.
      - data_inizio / data_fine: intervallo per la data.
      - ora_inizio / ora_fine: intervallo per l'ora.
      - durata_inizio / durata_fine: intervallo per la durata in minuti.
    """
    # Inizializza la QuerySet ordinata per codice sala e data
    qs = FasciaOraria.objects.all().order_by('sala', 'data', 'ora')

    # Lettura parametri GET dai filtri in fasce_orarie.html
    sala = request.GET.get('sala', '').strip()
    data_inizio = request.GET.get('data_inizio', '').strip()
    data_fine = request.GET.get('data_fine', '').strip()
    ora_inizio = request.GET.get('ora_inizio', '').strip()
    ora_fine = request.GET.get('ora_fine', '').strip()
    durata_inizio = request.GET.get('durata_inizio', '').strip()
    durata_fine = request.GET.get('durata_fine', '').strip()

    # Applicazione filtri
    if sala:
        qs = qs.filter(sala__codice__icontains=sala)
    if data_inizio:
        qs = qs.filter(data__gte=data_inizio)
    if data_fine:
        qs = qs.filter(data__lte=data_fine)
    if ora_inizio:
        qs = qs.filter(ora__gte=ora_inizio)
    if ora_fine:
        qs = qs.filter(ora__lte=ora_fine)
    if durata_inizio:
        try:
            durata_inizio_int = int(durata_inizio)
            qs = qs.filter(durata__gte=durata_inizio_int)
        except ValueError:
            pass 
    if durata_fine:
        try:
            durata_fine_int = int(durata_fine)
            qs = qs.filter(durata__lte=durata_fine_int)
        except ValueError:
            pass

    # conteggio dei risultati
    total_results = qs.count()

    # Raccolta dati per il template
    fasce_orarie_data = []
    for fascia in qs:
        # Estrae codice sala dal formato "(S022) - Nome Sala"
        match = re.search(r'\(([^)]+)\)', str(fascia.sala))
        codice_sala = match.group(1) if match else ''

        fasce_orarie_data.append({
            "sala": fascia.sala,
            "codice_sala": codice_sala,
            "data": fascia.data,
            "ora": fascia.ora,
            "durata": fascia.durata, # Sarà un intero (minuti)
        })

    # Manteniamo i valori della form per riempire i campi
    filters = {
        'sala': sala,
        'data_inizio': data_inizio,
        'data_fine': data_fine,
        'ora_inizio': ora_inizio,
        'ora_fine': ora_fine,
        'durata_inizio': durata_inizio,
        'durata_fine': durata_fine,
    }

    return render(request, "fasce_orarie/fasce_orarie.html", {
        "fasce_orarie_data": fasce_orarie_data,
        "filters": filters,
        "total_results": total_results,
    })