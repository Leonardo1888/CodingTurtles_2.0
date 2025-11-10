from django.shortcuts import render
from clienti.models import Abbonamento
from django.utils.timezone import now
import re
from django.db.models import Q

def index(request):
    abbonamenti = Abbonamento.objects.all().order_by('nAbb')
        
    nAbb = request.GET.get('nAbb', '').strip()
    cliente = request.GET.get('cliente', '').strip()
    inizio_min = request.GET.get('inizio_abbonamento_min', '').strip()
    inizio_max = request.GET.get('inizio_abbonamento_max', '').strip()
    fine_min = request.GET.get('fine_abbonamento_min', '').strip()
    fine_max = request.GET.get('fine_abbonamento_max', '').strip()
    prezzo_min = request.GET.get('prezzo_min', '').strip()
    prezzo_max = request.GET.get('prezzo_max', '').strip()
    attivi = request.GET.get('attivi')  # checkbox → "on" se selezionata

    if nAbb:
        abbonamenti = abbonamenti.filter(nAbb__icontains=nAbb)
    if cliente:
        abbonamenti = abbonamenti.filter(
            Q(cliente__codice__icontains=cliente) |
            Q(cliente__nome__icontains=cliente) |
            Q(cliente__cognome__icontains=cliente)
        )
    if inizio_min:
        abbonamenti = abbonamenti.filter(inizio__gte=inizio_min)
    if inizio_max:
        abbonamenti = abbonamenti.filter(inizio__lte=inizio_max)
    if fine_min:
        abbonamenti = abbonamenti.filter(fine__gte=fine_min)
    if fine_max:
        abbonamenti = abbonamenti.filter(fine__lte=fine_max)
    if prezzo_min:
        abbonamenti = abbonamenti.filter(prezzo__gte=prezzo_min)
    if prezzo_max:
        abbonamenti = abbonamenti.filter(prezzo__lte=prezzo_max)
    if attivi:
        from django.utils import timezone
        oggi = timezone.now().date()
        abbonamenti = abbonamenti.filter(inizio__lte=oggi, fine__gte=oggi)

    # --- Costruzione dati per il template ---
    abbonamenti_data = []
    for a in abbonamenti:
        # Estrae codice cliente dal formato "Nome Cognome (C123)"
        match = re.search(r'\(([^)]+)\)', str(a.cliente))
        codice_cliente = match.group(1) if match else ''

        abbonamenti_data.append({
            "nAbb": a.nAbb,
            "cliente": a.cliente,
            "codice_cliente": codice_cliente,
            "inizio": a.inizio,
            "fine": a.fine,
            "prezzo": a.prezzo,
        })

    filters = {
        'nAbb': nAbb,
        'cliente': cliente,
        'inizio_abbonamento_min': inizio_min,
        'inizio_abbonamento_max': inizio_max,
        'fine_abbonamento_min': fine_min,
        'fine_abbonamento_max': fine_max,
        'prezzo_min': prezzo_min,
        'prezzo_max': prezzo_max,
        'attivi': attivi,
    }

    return render(request, "abbonamenti/abbonamenti.html", {
        "abbonamenti_data": abbonamenti_data,
        "filters": filters,
    })
