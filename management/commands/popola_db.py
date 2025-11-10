import random
from datetime import datetime, timedelta, time
from django.db.utils import IntegrityError
from django.db import transaction

# --- 1. IMPORT DEI MODELLI DJANGO ---
from clienti.models import Cliente, Abbonamento, SubAbbonamento
from sale.models import Sala, FasciaOraria, Prenotazione, Posto


# --- FUNZIONE PER GENERARE UN CODICE FISCALE REALISTICO ---
def genera_cf(nome, cognome, data_nas_str):
    """
    Genera un Codice Fiscale strutturato in modo realistico ma con
    codice comune e carattere di controllo casuali.
    """
    # Mappa per la conversione del mese
    mesi_map = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'H', 7: 'L', 8: 'M', 9: 'P', 10: 'R', 11: 'S', 12: 'T'}

    # 1. Cognome (3 lettere) - Semplificato prendendo le prime 3 consonanti
    def get_cf_chars(s, is_consonant):
        s = s.upper().replace(" ", "")
        chars = ''.join(c for c in s if c.isalpha() and (c in 'BCDFGHJKLMNPQRSTVWXYZ' if is_consonant else c in 'AEIOU'))
        return chars.ljust(3, 'X')[:3]

    cf_cognome = get_cf_chars(cognome, True)

    # 2. Nome (3 lettere) - Semplificato (stessa logica)
    cf_nome = get_cf_chars(nome, True)

    try:
        data_dt = datetime.strptime(data_nas_str, '%Y-%m-%d')
    except ValueError:
        return "CFNONSIMULATO" # Fallback

    # 3. Anno di nascita (ultime 2 cifre)
    cf_anno = str(data_dt.year)[-2:]

    # 4. Mese di nascita (1 lettera dalla mappa)
    cf_mese = mesi_map[data_dt.month]

    # 5. Giorno di nascita e sesso (2 cifre)
    sesso = random.choice(['M', 'F'])
    giorno = data_dt.day
    if sesso == 'F':
        giorno += 40
    cf_giorno = f"{giorno:02d}"

    # 6. Comune di nascita (4 caratteri) - Simulato
    cf_comune = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') + ''.join(random.choices('0123456789', k=3))

    # 7. Carattere di controllo (1 lettera) - Simulato
    cf_controllo = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    return f"{cf_cognome}{cf_nome}{cf_anno}{cf_mese}{cf_giorno}{cf_comune}{cf_controllo}"


# --- CONFIGURAZIONE ---
NUM_SALE = 50
NUM_CLIENTI = 250
NUM_GIORNI_DA_POPOLARE = 7 # Popoliamo per una settimana
START_DATE_PRENOTAZIONI = datetime(2025, 6, 1)

# --- DATI DI ESEMPIO ---
nomi = ['Mario', 'Luigi', 'Anna', 'Giovanni', 'Sofia', 'Francesco', 'Alessia', 'Luca', 'Martina', 'Andrea', 'Antonio', 'Leonardo', 'Fabio', 'Riccardo', "Maurizio"]
cognomi = ['Rossi', 'Verdi', 'Bianchi', 'Neri', 'Gialli', 'Marroni', 'Arancioni', 'Rosa', 'Viola', 'Blu']
temi = ['Cardio', 'Pesi liberi', 'Macchine', 'Corpo libero', 'Sauna']
sottocategorie_per_tema = {
    'Cardio': ['Tapis roulant', 'Sala da ballo', 'Ellittica'],
    'Pesi liberi': ['Manubri', 'Bilancieri', 'Kettlebell'],
    'Macchine': ['Lat machine', 'Leg press', 'Chest press'],
    'Corpo libero': ['Tappetini', 'Bande elastiche', 'Sbarre per trazioni'],
    'Sauna': ['Sauna finlandese', 'Sauna a infrarossi', 'Bagno turco']
}
mq_values = [50, 80, 100, 150, 200]
prezzo_durata_map = {
    50: 30,    # Mensile
    100: 90,   # Trimestrale
    150: 180,  # Semestrale
    200: 365   # Annuale
}
possible_prices = list(prezzo_durata_map.keys())


# --- STRUTTURE DATI PER MEMORIZZARE GLI OGGETTI DJANGO GENERATI ---
# Useremo i dizionari per un accesso rapido in base alla chiave
generated_sale = {}
generated_clienti = {}
generated_abbonamenti = []
generated_fasce_orarie = []
generated_posti = []
generated_prenotazioni = []
generated_sub_abbonamenti = []

# Usiamo un blocco transaction per garantire che tutte le operazioni siano atomiche
with transaction.atomic():

    # --- 2. SVUOTAMENTO TABELLE (con l'ORM) ---
    print("--- SVUOTAMENTO TABELLE ---")
    SubAbbonamento.objects.all().delete()
    Prenotazione.objects.all().delete()
    Abbonamento.objects.all().delete()
    Cliente.objects.all().delete()
    Posto.objects.all().delete()
    FasciaOraria.objects.all().delete()
    Sala.objects.all().delete()
    print("Svuotamento completato.")

    # --- 3. POPOLAMENTO Sala ---
    print("--- POPOLAMENTO Sala ---")
    sala_codici = [f"S{i:03d}" for i in range(1, NUM_SALE + 1)]
    for i, codice in enumerate(sala_codici):
        tema = temi[i % len(temi)]
        sottocategoria_list = sottocategorie_per_tema[tema]
        sottocategoria = sottocategoria_list[i % len(sottocategoria_list)]
        nome = f"Sala {sottocategoria}"
        mq = random.choice(mq_values)
        
        # Creazione OGGETTO DJANGO
        sala_obj = Sala.objects.create(
            codice=codice,
            nome=nome,
            tema=tema,
            mq=mq
        )
        generated_sale[codice] = sala_obj # Salviamo l'oggetto per le FK

    print(f"- Sale: {len(generated_sale)}")


    # --- 4. POPOLAMENTO Cliente ---
    print("--- POPOLAMENTO Cliente ---")
    clienti_codici = [f"C{i:03d}" for i in range(1, NUM_CLIENTI + 1)]
    for codice in clienti_codici:
        nome = random.choice(nomi)
        cognome = random.choice(cognomi)
        # Genera data e CF
        data_nas = (datetime(1970, 1, 1) + timedelta(days=random.randint(0, 11000))).date() # Usiamo .date() per consistenza
        cf = genera_cf(nome, cognome, data_nas.strftime('%Y-%m-%d'))
        
        indirizzo = f"{random.randint(1, 100)} Via {random.choice(['Roma', 'Milano', 'Napoli', 'Torino', 'Palermo'])}"
        tel = ''.join(random.choices('0123456789', k=9))
        email = f"{nome.lower()}.{cognome.lower()}{random.randint(10,99)}@example.com"
        
        # Creazione OGGETTO DJANGO
        cliente_obj = Cliente.objects.create(
            codice=codice,
            nome=nome,
            cognome=cognome,
            cf=cf,
            dataNas=data_nas,
            indirizzo=indirizzo,
            tel=tel,
            email=email
        )
        generated_clienti[codice] = cliente_obj # Salviamo l'oggetto per le FK

    print(f"- Clienti: {len(generated_clienti)}")


    # --- 5. POPOLAMENTO Abbonamento ---
    print("--- POPOLAMENTO Abbonamento ---")
    clienti_con_abbonamento = random.sample(list(generated_clienti.keys()), int(len(generated_clienti) * 0.8))
    
    for i, codice_cliente in enumerate(clienti_con_abbonamento):
        n_abb = f"A{i+1:03d}"
        
        inizio = (datetime(2025, 1, 1) + timedelta(days=random.randint(0, 150))).date()
        prezzo = random.choice(possible_prices)
        durata_giorni = prezzo_durata_map[prezzo]
        fine = inizio + timedelta(days=durata_giorni)
        
        cliente_obj = generated_clienti[codice_cliente] # Recupera l'oggetto Cliente
        
        # Creazione OGGETTO DJANGO
        abbonamento_obj = Abbonamento.objects.create(
            nAbb=n_abb, 
            cliente=cliente_obj, # Usa l'oggetto Cliente
            inizio=inizio, 
            fine=fine, 
            prezzo=prezzo
        )
        generated_abbonamenti.append(abbonamento_obj)

    print(f"- Abbonamenti: {len(generated_abbonamenti)}")


    # --- 6. POPOLAMENTO FasciaOraria ---
    print("--- POPOLAMENTO FasciaOraria ---")
    for sala_obj in generated_sale.values():
        for i in range(NUM_GIORNI_DA_POPOLARE):
            current_date = (START_DATE_PRENOTAZIONI + timedelta(days=i)).date()
            start_hour = 8
            while start_hour < 20:
                max_durata = min(3, 20 - start_hour)
                if max_durata < 1:
                    break
                durata = random.randint(1, max_durata)
                ora_obj = time(start_hour, 0) # Oggetto time Python
                
                # Creazione OGGETTO DJANGO
                fascia_obj = FasciaOraria.objects.create(
                    sala=sala_obj, # Usa l'oggetto Sala
                    data=current_date, 
                    ora=ora_obj, # Usa l'oggetto time
                    durata=durata
                )
                generated_fasce_orarie.append(fascia_obj)
                
                # Aggiungiamo i dati necessari per Posto
                fascia_obj.mq = sala_obj.mq # Aggiungiamo l'attributo mq per uso interno
                
                start_hour += durata

    print(f"- Fasce Orarie: {len(generated_fasce_orarie)}")


    # --- 7. POPOLAMENTO Posto ---
    print("--- POPOLAMENTO Posto ---")
    for fascia_obj in generated_fasce_orarie:
        # Numero di posti in base ai mq della sala (es. 1 posto ogni 10mq)
        # Nota: fascia_obj ha l'attributo .sala che è l'oggetto Sala
        num_posti = max(1, fascia_obj.sala.mq // 10) 
        for n_prog in range(1, num_posti + 1):
            
            # Creazione OGGETTO DJANGO
            posto_obj = Posto.objects.create(
                sala=fascia_obj.sala,
                data=fascia_obj.data,
                ora=fascia_obj.ora,
                nProg=n_prog, 
            )
            # Salviamo un record per l'uso nelle Prenotazioni
            generated_posti.append({'obj': posto_obj, 'nProg_interno': n_prog, 'fascia': fascia_obj})

    print(f"- Posti: {len(generated_posti)}")


    # --- 8. POPOLAMENTO Prenotazione & SubAbbonamento ---
    print("--- POPOLAMENTO Prenotazione & SubAbbonamento ---")
    abbonamenti_per_cliente = {}
    for abb in generated_abbonamenti:
        codice_cliente = abb.cliente.codice
        if codice_cliente not in abbonamenti_per_cliente:
            abbonamenti_per_cliente[codice_cliente] = []
        abbonamenti_per_cliente[codice_cliente].append(abb)
        
    posti_da_prenotare = random.sample(generated_posti, int(len(generated_posti) * 0.3))

    for posto_dict in posti_da_prenotare:
        posto_obj_fk = posto_dict['obj']
        fascia_obj = posto_dict['fascia']
        nProg_interno = posto_dict['nProg_interno']

        # 1. Troviamo un cliente casuale che non abbia già prenotato in questa fascia
        while True:
            cliente_casuale_codice = random.choice(list(generated_clienti.keys()))
            # Simuliamo il controllo di unicità (cliente, data, ora)
            key = (cliente_casuale_codice, fascia_obj.data, fascia_obj.ora)
            # Nota: questo script non implementa il controllo per evitare doppie prenotazioni, ma lo faremmo se stessimo popolando la Prenotazione come chiave unica su (cliente, sala, data, ora)
            break 
            
        cliente_obj = generated_clienti[cliente_casuale_codice]

        abb_to_add = 'nessuno' 
        abbonamento_usato_obj = None 

        # 2. Controlla e associa un abbonamento valido
        if cliente_casuale_codice in abbonamenti_per_cliente:
            abbonamenti_validi = [
                abb for abb in abbonamenti_per_cliente[cliente_casuale_codice]
                if abb.inizio <= fascia_obj.data <= abb.fine
            ]
            
            if abbonamenti_validi:
                abbonamento_usato_obj = random.choice(abbonamenti_validi)
                abb_to_add = abbonamento_usato_obj.nAbb

        # 3. Creazione record Prenotazione
        prenotazione_obj = Prenotazione.objects.create(
            cliente=cliente_obj.codice, # Campo CharField, usiamo il codice
            sala=fascia_obj.sala,      # Oggetto Sala
            data=fascia_obj.data,
            ora=fascia_obj.ora,
            posto=nProg_interno,       # Numero del posto (non l'ID della tabella Posto)
            abbonamento=abb_to_add     # Campo CharField, usiamo il codice
        )
        generated_prenotazioni.append(prenotazione_obj)

        # 4. Creazione record SubAbbonamento (solo se abbiamo usato un abbonamento valido)
        if abbonamento_usato_obj:
            SubAbbonamento.objects.create(
                prenotazione=prenotazione_obj.nProg, # ID auto-generato della Prenotazione
                abbonamento=abbonamento_usato_obj.nAbb # Codice CharField
            )
            generated_sub_abbonamenti.append(SubAbbonamento)


    print(f"- Prenotazioni: {len(generated_prenotazioni)}")
    print(f"- SubAbbonamenti: {len(generated_sub_abbonamenti)}")
    print("\nFile di popolazione completato con successo tramite ORM di Django!")


# --- ESECUZIONE ---
# Per eseguire questo script, usare terminale nella root progetto
#
# $ python manage.py shell
# >>> exec(open('management/commands/popola_db.py').read())
# >>> exit()