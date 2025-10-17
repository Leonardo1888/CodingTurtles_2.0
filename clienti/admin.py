from django.contrib import admin
from .models import Cliente, Abbonamento, SubAbbonamento

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('codice', 'nome', 'cognome', 'email', 'tel')
    search_fields = ('codice', 'nome', 'cognome', 'cf', 'email')
    list_filter = ('dataNas',)
    ordering = ('cognome', 'nome')

class AbbonamentoAdmin(admin.ModelAdmin):
    list_display = ('nAbb', 'cliente', 'inizio', 'fine', 'prezzo')
    search_fields = ('nAbb', 'cliente')
    list_filter = ('inizio', 'fine')
    ordering = ('-fine',)
    raw_id_fields = ('cliente',)

class SubAbbonamentoAdmin(admin.ModelAdmin):
    list_display = ('prenotazione', 'abbonamento')
    search_fields = ('prenotazione', 'abbonamento')
    list_filter = ('prenotazione', 'abbonamento')
    ordering = ('prenotazione',)

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Abbonamento, AbbonamentoAdmin)
admin.site.register(SubAbbonamento, SubAbbonamentoAdmin)
