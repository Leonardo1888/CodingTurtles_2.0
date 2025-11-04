from django.shortcuts import render
from sale.models import FasciaOraria

def fasce_orarie(request, codice_sala):
    fasce_orarie = FasciaOraria.objects.filter(sala__codice=codice_sala)
    return render(request, "fasce_orarie/fasce_orarie.html", {'fasce_orarie_data': fasce_orarie})