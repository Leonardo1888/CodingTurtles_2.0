from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "fasce_orarie/fasce_orarie.html")