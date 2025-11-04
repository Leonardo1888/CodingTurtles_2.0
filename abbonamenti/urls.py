from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:codice_cliente>/", views.abbonamenti, name="abbonamenti"), #aggiunto per collegamento cliente -> n.abb. views.abbonamenti è la funzione in views
                                                                            #con parametro codice_cliente aggiuntivo
]