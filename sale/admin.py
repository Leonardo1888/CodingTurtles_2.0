from django.contrib import admin
from .models import Sala, FasciaOraria, Prenotazione, Posto

class SalaAdmin(admin.ModelAdmin):
    list_display = ('codice', 'nome', 'tema', 'mq')  # Campi da mostrare nella lista
    search_fields = ('codice', 'nome', 'tema', 'mq')  # Campi su cui effettuare la ricerca
    list_filter = ('codice', 'nome', 'tema', 'mq')  # Filtri laterali
    ordering = ('codice',)  # Ordinamento di default

class FasciaOrariaAdmin(admin.ModelAdmin):
    list_display = ('sala', 'data', 'ora', 'durata')  # Campi da mostrare nella lista
    search_fields = ('sala', 'data', 'ora', 'durata')  # Campi su cui effettuare la ricerca
    list_filter = ('sala', 'data', 'ora', 'durata')  # Filtri laterali
    ordering = ('sala', 'data', 'ora')  # Ordinamento di default

class PrenotazioneAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'sala', 'data', 'ora', 'posto', 'abbonamento')  # Campi da mostrare nella lista
    search_fields = ('cliente', 'sala', 'data', 'ora', 'posto', 'abbonamento')  # Campi su cui effettuare la ricerca
    list_filter = ('cliente', 'sala', 'data', 'ora', 'posto', 'abbonamento')  # Filtri laterali
    ordering = ('nProg',)  # Ordinamento di default

class PostoAdmin(admin.ModelAdmin):
    list_display = ('nProg', 'sala', 'data', 'ora')  # Campi da mostrare nella lista
    search_fields = ('nProg', 'sala', 'data', 'ora')  # Campi su cui effettuare la ricerca
    list_filter = ('nProg', 'sala', 'data', 'ora')  # Filtri laterali
    ordering = ('nProg',)  # Ordinamento di default

admin.site.register(Sala, SalaAdmin)
admin.site.register(FasciaOraria, FasciaOrariaAdmin)
admin.site.register(Prenotazione, PrenotazioneAdmin)
admin.site.register(Posto, PostoAdmin)