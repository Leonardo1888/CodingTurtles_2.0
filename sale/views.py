from django.shortcuts import render
from django.http import HttpResponse

def sale(request):
    return render(request, "sale/sale.html")