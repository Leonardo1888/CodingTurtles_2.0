from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from .models import Sala, FasciaOraria, Prenotazione

@csrf_exempt
def sale_create(request):
    """Crea una nuova sala via POST AJAX."""
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Metodo non consentito"}, status=405)

    import json
    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST

    codice = (data.get("codice") or "").strip()
    nome = (data.get("nome") or "").strip()
    tema = (data.get("tema") or "").strip()
    mq = data.get("mq")

    errors = []
    if not nome:
        errors.append("Il nome della sala è obbligatorio")
    if not tema:
        errors.append("Il tema è obbligatorio")
    try:
        mq = int(mq)
        if mq <= 0 or mq > 1000:
            errors.append("I metri quadrati devono essere tra 1 e 1000")
    except Exception:
        errors.append("I metri quadrati devono essere un numero valido")

    # Codice: se non fornito, genera il prossimo disponibile
    if not codice:
        # Trova il primo codice libero SNNN
        existing = set(Sala.objects.values_list('codice', flat=True))
        n = 1
        while True:
            c = f"S{n:03d}"
            if c not in existing:
                codice = c
                break
            n += 1
    else:
        if not codice.startswith("S") or not codice[1:].isdigit() or len(codice) != 4:
            errors.append("Il codice deve essere nel formato S001, S002, ecc.")
        if Sala.objects.filter(codice=codice).exists():
            errors.append(f"Il codice sala '{codice}' esiste già")

    if errors:
        return JsonResponse({"success": False, "message": ", ".join(errors)})

    sala = Sala(codice=codice, nome=nome, tema=tema, mq=mq)
    sala.save()
    return JsonResponse({"success": True, "message": f"Sala '{codice}' aggiunta con successo", "data": {"codice": codice, "nome": nome, "tema": tema, "mq": mq}})


@csrf_exempt
def sale_update(request):
    """Aggiorna una sala via POST AJAX."""
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Metodo non consentito"}, status=405)
    import json
    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST
    codice = (data.get("codice") or "").strip()
    nome = (data.get("nome") or "").strip()
    tema = (data.get("tema") or "").strip()
    mq = data.get("mq")
    if not codice:
        return JsonResponse({"success": False, "message": "Codice sala mancante"})
    try:
        sala = Sala.objects.get(codice=codice)
    except Sala.DoesNotExist:
        return JsonResponse({"success": False, "message": f"Sala '{codice}' non trovata"})
    errors = []
    if not nome:
        errors.append("Il nome della sala è obbligatorio")
    if not tema:
        errors.append("Il tema è obbligatorio")
    try:
        mq = int(mq)
        if mq <= 0 or mq > 1000:
            errors.append("I metri quadrati devono essere tra 1 e 1000")
    except Exception:
        errors.append("I metri quadrati devono essere un numero valido")
    if errors:
        return JsonResponse({"success": False, "message": ", ".join(errors)})
    sala.nome = nome
    sala.tema = tema
    sala.mq = mq
    sala.save()
    return JsonResponse({"success": True, "message": f"Sala '{codice}' aggiornata con successo", "data": {"codice": codice, "nome": nome, "tema": tema, "mq": mq}})

@csrf_exempt
def sale_delete(request):
    """Elimina una sala via POST AJAX."""
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Metodo non consentito"}, status=405)
    import json
    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST
    codice = (data.get("codice") or "").strip()
    if not codice:
        return JsonResponse({"success": False, "message": "Codice sala mancante"})
    try:
        sala = Sala.objects.get(codice=codice)
    except Sala.DoesNotExist:
        return JsonResponse({"success": False, "message": f"Sala '{codice}' non trovata"})
    sala.delete()
    return JsonResponse({"success": True, "message": f"Sala '{codice}' eliminata con successo"})

def index(request):
    """Lista sale con filtro via GET.

    Supporta i parametri GET:
      - Codice: ricerca codice sala (icontains)
      - Nome: ricerca sul nome (icontains)
      - Tema: filtro esatto sul tema
      - Mq_min / Mq_max: intervallo per metri quadrati
    """
    qs = Sala.objects.all().order_by('codice')

    # lettura parametri GET
    codice = request.GET.get('Codice', '').strip()
    nome = request.GET.get('Nome', '').strip()
    tema = request.GET.get('Tema', '').strip()
    mq_min = request.GET.get('Mq_min', '').strip()
    mq_max = request.GET.get('Mq_max', '').strip()

    if codice:
        qs = qs.filter(codice__icontains=codice)
    if nome:
        qs = qs.filter(nome__icontains=nome)
    if tema:
        qs = qs.filter(tema=tema)
    if mq_min:
        try:
            qs = qs.filter(mq__gte=int(mq_min))
        except ValueError:
            pass
    if mq_max:
        try:
            qs = qs.filter(mq__lte=int(mq_max))
        except ValueError:
            pass

    # raccolta dati per il template
    sale_data = []
    for sala in qs:
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

    # valori distinti per il select Tema
    themes = Sala.objects.order_by('tema').values_list('tema', flat=True).distinct()

    # manteniamo i valori della form per riempire i campi
    filters = {
        'Codice': codice,
        'Nome': nome,
        'Tema': tema,
        'Mq_min': mq_min,
        'Mq_max': mq_max,
    }

    return render(request, "sale/sale.html", {"sale_data": sale_data, "themes": themes, "filters": filters})