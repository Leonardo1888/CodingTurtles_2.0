from django.db import models

class Cliente(models.Model): # codice, nome, cognome, cf, dataNas, indirizzo, tel, email
    codice = models.CharField(
        max_length=5, # Aumentato a 5 per codici come C001
        primary_key=True,
        verbose_name="Codice Cliente",
        unique=True
    ) 
    
    nome = models.CharField(max_length=50, verbose_name="Nome")
    cognome = models.CharField(max_length=50, verbose_name="Cognome")
    cf = models.CharField(max_length=16, verbose_name="Codice Fiscale")
    dataNas = models.DateField(verbose_name="Data di nascita")
    indirizzo = models.CharField(max_length=128, verbose_name="Indirizzo")
    tel = models.CharField(max_length=24, verbose_name="Telefono")
    email = models.EmailField(max_length=64, verbose_name="E-mail") 

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clienti"
        ordering = ['cognome', 'nome']

    def __str__(self):
        return f"{self.cognome} {self.nome} ({self.codice})"

class Abbonamento(models.Model): # nAbb, cliente inizio, fine, prezzo
    nAbb = models.CharField(
        max_length=5, # Esempio A001
        primary_key=True, 
        verbose_name="Numero Abbonamento",
        default="null",
        unique=True
    ) 
    
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE,
        verbose_name="Cliente",
        related_name="abbonamenti" # Nome per l'accesso inverso (cliente.abbonamenti.all())
    )
    
    inizio = models.DateField(verbose_name="Data di inizio")
    fine = models.DateField(verbose_name="Data di fine")
    prezzo = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Prezzo abbonamento")

    class Meta:
        verbose_name = "Abbonamento"
        verbose_name_plural = "Abbonamenti"
        ordering = ['-fine']

    def __str__(self):
        return f"Abbonamento #{self.nAbb} di {self.cliente.cognome}"

class SubAbbonamento(models.Model): # prenotazione, abbonamento

    prenotazione = models.CharField(max_length=10, verbose_name="Prenotazione")
    abbonamento = models.CharField(max_length=10, verbose_name="Abbonamento")

    class Meta:
        verbose_name = "SubAbbonamento"
        verbose_name_plural = "SubAbbonamenti"

    def __str__(self):
        return f"Abbonamento #{self.abbonamento} della prenotaz. {self.prenotazione}"
