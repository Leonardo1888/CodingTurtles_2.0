from django.db import models

class Sala(models.Model): # codice, nome, tema, mq
    codice = models.CharField(max_length=4, primary_key=True, verbose_name="Codice Sala", unique=True)
    nome = models.CharField(max_length=100, verbose_name="Nome")
    tema = models.CharField(max_length=50, verbose_name="Tema")
    mq = models.IntegerField(verbose_name="Metri Quadri")

    class Meta:
        verbose_name_plural = "Sale"
        ordering = ['codice']  # Ordina le sale per codice di default

    def __str__(self):
        return f"({self.codice}) - {self.nome}"

class FasciaOraria(models.Model): # sala, data, ora, durata

    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, verbose_name="Sala")
    data = models.DateField(verbose_name="Data")
    ora = models.TimeField(verbose_name="Ora")
    durata = models.IntegerField(verbose_name="Durata (in minuti)")

    class Meta:
        verbose_name_plural = "Fasce Orarie"
        # Ordina per data e ora, che è più logico
        ordering = ['data', 'ora']

    def __str__(self):
        return f"Fascia oraria {self.sala} - {self.data} ore {self.ora}"

class Prenotazione(models.Model): # nProg, cliente, sala, data, ora, posto, abbonamento
    nProg = models.AutoField(primary_key=True, verbose_name="Numero Progressivo", unique=True)
    
    cliente = models.CharField(max_length=4, verbose_name="Codice Cliente")
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, verbose_name="Codice Sala")
    
    data = models.DateField(verbose_name="Data")
    ora = models.TimeField(verbose_name="Ora")
    posto = models.IntegerField(verbose_name="Posto")
  
    abbonamento = models.CharField(max_length=100, verbose_name="Codice Abbonamento")

    class Meta:
        verbose_name_plural = "Prenotazioni"
        ordering = ['sala']  # Ordina le prenotazioni per sala

    def __str__(self):
        return f"Prenotazione {self.nProg} per {self.cliente} in {self.sala}"

class Posto(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, verbose_name="Codice Sala")
    data = models.DateField(verbose_name="Data")
    ora = models.TimeField(verbose_name="Ora")
    nProg = models.IntegerField(verbose_name="Numero Progressivo")
  
    class Meta:
        verbose_name_plural = "Posti"
        ordering = ['sala']  # Ordina le prenotazioni per sala
        unique_together = ('sala', 'data', 'ora', 'nProg')

    def __str__(self):
        return f"{self.sala} il {self.data} alle {self.ora}, posto {self.nProg}"

