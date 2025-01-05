# Crea file PDF formato A4 a 72 DPI dimensioni x=595 y=842 pixels

Partendo da una bozza di programma con AI e successive modifiche e integrazioni.

## Calendario con 1 mese ogni pagina in 2 colonne

## Giorni festivi in Rosso leggendoli da tabella allegata

## Santo del giorno leggendoli da tabella allegata

## Calcolo delle Fasi lunari da libreria allegata preso da:
_____________________________________________________________________
http://navigazione.altervista.org/python-fasi-lunari/
versione 24.2.19
Nanni Manca
Carloforte, Sardegna
email: nmanca@tiscali.it
calcoli originali: Ernest William Brown
__________________________________________________________
la mia modifica è stata di convertire le procedure in funzioni  togliendo le variabili globali

> [!NOTE]
Dopo aver caricato da Festivi.txt le date dei giorni festivi calcola la data della Pasqua e la inserisce neldizionario.

### File allegati
- **Calendar_PDF_UI.py**  MAIN interfaccia grafica 
- **faseluna.py**  Calcola le fasi lunari dell'anno indicato          
- **calendarPDF.py**  Crea il file PDF
- **Santi.txt**  Dati per creare il dizionario dei nomi dei Santi
- **Festivi.txt**  Dati per creare il dizionario delle festività

### Libreria necessaria per creare il file PDF
- reportlab

### esempi di calendari 
dal 2024 al 1030
e immagine di un mese "2030-gennaio.png"
