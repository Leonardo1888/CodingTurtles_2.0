from django.shortcuts import render
from .models import Cliente, Abbonamento
from sale.models import Prenotazione

def index(request):
    """Lista clienti con filtro via GET.

    Supporta i parametri GET:
      - Codice, Nome, Cognome, Cf: ricerca parziale (icontains)
      - DataNas_min / DataNas_max: intervallo per data di nascita
      - Indirizzo, Tel, Email: ricerca parziale (icontains)
    """
    qs = Cliente.objects.all().order_by('codice')

    # lettura parametri GET
    codice = request.GET.get('Codice', '').strip()
    nome = request.GET.get('Nome', '').strip()
    cognome = request.GET.get('Cognome', '').strip()
    cf = request.GET.get('Cf', '').strip()
    dataNas_min = request.GET.get('DataNas_min', '').strip()
    dataNas_max = request.GET.get('DataNas_max', '').strip()
    indirizzo = request.GET.get('Indirizzo', '').strip()
    tel = request.GET.get('Tel', '').strip()
    email = request.GET.get('Email', '').strip()
    haAbbonamento = request.GET.get('HaAbbonamento', '').strip()
    
    # applicazione filtri
    if codice:
        qs = qs.filter(codice__icontains=codice)
    if nome:
        qs = qs.filter(nome__icontains=nome)
    if cognome:
        qs = qs.filter(cognome__icontains=cognome)
    if cf:
        qs = qs.filter(cf__icontains=cf)
    if dataNas_min:
        qs = qs.filter(dataNas__gte=dataNas_min)
    if dataNas_max:
        qs = qs.filter(dataNas__lte=dataNas_max)
    if indirizzo:
        qs = qs.filter(indirizzo__icontains=indirizzo)
    if tel:
        qs = qs.filter(tel__icontains=tel)
    if email:
        qs = qs.filter(email__icontains=email)

    # raccolta dati per il template
    clienti_data = []
    for cliente in qs:
        n_abb = Abbonamento.objects.filter(cliente=cliente).count()
        n_prenotazioni = Prenotazione.objects.filter(cliente=cliente.codice).count()
        
        if haAbbonamento and n_abb == 0:
            continue
        
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

    # conteggio dei risultati
    total_results = len(clienti_data)
    
    # manteniamo i valori della form per riempire i campi
    filters = {
        'Codice': codice,
        'Nome': nome,
        'Cognome': cognome,
        'Cf': cf,
        'DataNas_min': dataNas_min,
        'DataNas_max': dataNas_max,
        'Indirizzo': indirizzo,
        'Tel': tel,
        'Email': email,
        'HaAbbonamento': haAbbonamento,
    }

    return render(request, "clienti/clienti.html", {
        "clienti_data": clienti_data,
        "filters": filters,
        "total_results": total_results,
    })
