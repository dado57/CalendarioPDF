# Partendo da una bozza di programma con AI e successive modifiche e integrazioni.

# Crea file PDF formato A4 a 72 DPI dimensioni x=595 y=842 pixels

# Calendario con 1 mese ogni pagina in 2 colonne

# Giorni festivi in Rosso leggendoli da tabella allegata

# Santo del giorno leggendoli da tabella allegata

# Calcolo delle Fasi lunari da libreria allegata preso da:
_____________________________________________________________________
http://navigazione.altervista.org/python-fasi-lunari/
versione 24.2.19
Nanni Manca
Carloforte, Sardegna
email: nmanca@tiscali.it
calcoli originali: Ernest William Brown
__________________________________________________________
la mia modifica è stata di convertire le procedure in funzioni  togliendo le variabili globali


Dopo aver caricato da Festivi.txt le date dei giorni festivi calcola la data della Pasqua.

File allegati
- Santi.txt
- Festivi.txt
- faseluna.py

Libreria necessaria per creare il file PDF
- reportlab
