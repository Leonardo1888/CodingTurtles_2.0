from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Ciao, sei nella pagina delle sale. Qui farai il crud di sale")