# calendarPDF.py
# Santi.txt (allegata)
# Festivi.txt (allegata)
# faseluna.py (allegata)
# reportlab (libreria non allegata)

# Crea file PDF formato A4 a 72 DPI dimensioni x=595 y=842 pixels
# Calendario 1 mese ogni pagina in 2 colonne
# Giorni festivi in Rosso leggendoli da tabella allegata
# Santo del giorno leggendoli da tabella allegata
# Fasi lunari da libreria allegata
# Calcolo della Pasqua interno a questo file

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, black, gray,blue,white

import csv
import calendar
from datetime import datetime,date, timedelta

import os
import sys

from faseluna import FasiAnno # ritorna dizionario FasiLuna

"""
Ritorna il percorso della directory contenente il file sorgente 
o l'eseguibile del programma compilato, con uno slash finale.
"""
path = sys.executable if getattr(sys, 'frozen', False) else __file__
directory = os.path.dirname(os.path.abspath(path))
percorso = os.path.join(directory, '')

#### Dizionario per i santi
file_path = percorso + "Santi.txt"
dSanti={} 
# Leggi il file CSV
with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for col in reader:
        if len(col) == 2:  # Se ci sono 2 colonne
            key, value = col[0], col[1]
            dSanti[key] = value

dFestivi={}

def leggi_festivi(percorso):
    #### Dizionario per i giorni Festivi
    file_path = percorso + "Festivi.txt"
    global dFestivi
    dFestivi={}
    # Leggi il file CSV
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for col in reader:
            if len(col) == 2:  # Se ci sono 2 colonne
                key, value = col[0], col[1]
                dFestivi[key] = value

def data_successiva(data_input):
    # Converti la stringa in un oggetto datetime
    data = datetime.strptime(data_input, "%d-%m-%Y") #21-04-2024
    # Aggiungi un giorno
    giorno_successivo = data + timedelta(days=1)
    # Converti di nuovo in stringa nel formato richiesto
    gs = giorno_successivo.strftime("%d-%m") # 21-04 
    return gs


def calcola_pasqua(anno):
    """
    Calcola la data della Pasqua cattolica per un dato anno utilizzando l'algoritmo di Gauss.
    :param anno: L'anno per cui calcolare la Pasqua.
    :return: Una stringa rappresentante la data della Pasqua (giorno e mese)
    e del Lunedi dell'Angelo.
    """
    if anno < 1583:
        raise ValueError("L'algoritmo funziona solo per anni successivi al 1582.")

    # Algoritmo di Gauss
    a = anno % 19
    b = anno // 100
    c = anno % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mese = (h + l - 7 * m + 114) // 31
    giorno = ((h + l - 7 * m + 114) % 31) + 1
    pasqua = f"{giorno:02d}-{mese:02d}-{anno:04d}"
    giorno_dopo = data_successiva(pasqua)
    return f"{giorno:02d}-{mese:02d}",f"{giorno_dopo}"

def scrivi_a(foglio,x,y,colore,testo,size,carattere):
    foglio.setFont(carattere, size)
    foglio.setFillColor(colore)
    foglio.drawString(x, y, testo)
    
def genera_pdf(anno, fFL = True, fSA=True, fFE=True):
    
    sOpt  = 'L' if fFL else ""
    sOpt += 'S' if fSA else ""
    sOpt += 'F' if fFE else ""
    
    nome_file = percorso + "Calen" + str(anno) + sOpt + ".pdf"
    
    dFasiLuna = FasiAnno(anno) # crea dFasiLuna
    
    # Calcolo data di pasqua
    leggi_festivi(percorso) # per ogni anno resetta la Pasqua
    pasqua,angelo = calcola_pasqua(anno)
    dFestivi[pasqua] = "Pasqua"
    dFestivi[angelo] = "Lunedi dell'Angelo"
    
    # Creazione del canvas per il PDF
    pdf = canvas.Canvas(nome_file, pagesize=A4)
    pdf.setTitle(f"Calendario {anno}")

    # Nomi dei mesi in italiano
    mesi_italiani = [
        "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
        "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"
    ]

    # Ottieni le informazioni mese per mese
    for mese in range(1, 13):
        
        pdf.setLineWidth(0.25) # Spessore linee 
        pdf.circle(595/2, 820, 7, stroke=1, fill=0)
        
        pdf.setLineWidth(1) 
        
        pdf.setFont("Helvetica-Bold", 60)
        nome_mese = mesi_italiani[mese - 1]
        pdf.drawCentredString(595/2, 760, f"{nome_mese} {anno}")
        
        y = 700
        ng = 0
        
        pdf.setStrokeColor(gray)
        pdf.line( 25,y+40,290,y+40)
        pdf.line(297,y+40,570,y+40)
        
        cal = calendar.monthcalendar(anno, mese)
        for settimana in cal:
            for idx, giorno in enumerate(settimana):
                nome_giorno = ["LUN", "MAR", "MER", "GIO", "VEN", "SAB", "DOM"]
                
                if giorno != 0:
                    r = ng % 16
                    c = ng // 16
                    ng += 1
                    
                    data_corrente = date(anno, mese, giorno).strftime("%d-%m")
                    festa = dFestivi.get(data_corrente, "")
                    santo = dSanti.get(data_corrente, "")
                    luna  = dFasiLuna.get(data_corrente, "") 
                    testo = ""
                    
                    colore = black
                    if idx == 6:
                        colore = red
                    if festa and fFE :
                        colore = red
                        testo = f"{festa}"
                    elif santo and fSA:
                        testo = f"{santo[:15]}"

                    xc = 25 + 275 * c
                    yc = 700 - r*40 + 1
                    
                    # numero del giorno
                    pdf.setFont("Helvetica-Bold", 50)
                    pdf.setFillColor(colore)
                    pdf.drawCentredString(xc+25, yc, f"{giorno}")
                    
                    # Nome del giorno della settimana
                    scrivi_a(pdf,xc+58,yc+22,colore,f"{nome_giorno[idx]}",14,"Helvetica")
                    
                    # Festivita o santo del giorno
                    if festa or santo:
                        scrivi_a(pdf,xc+58,yc,colore,f"{testo}",14,"Helvetica")
                    
                    if fFL :
                        # Disegna le fasi della luna
                        pdf.setFillColor(black)
                        pdf.setStrokeColor(black)
                        xc += 30
                        if luna == 'LN':
                            pdf.circle(xc+225,yc+20, 10, stroke=1, fill=1)
                        if luna == 'LP':
                            pdf.circle(xc+225,yc+20, 10, stroke=1, fill=0)
                        if luna == 'PQ':
                            pdf.wedge(xc+215,yc+10,xc+235, yc+30, 270,180, stroke=1, fill=0)
                        if luna == 'UQ':
                            pdf.wedge(xc+215,yc+10,xc+235, yc+30, 90,180, stroke=1, fill=0)
                        if luna:
                            scrivi_a(pdf,xc+217,yc,black,f"{luna}",10,"Helvetica")
                    
                    # Linea sotto il giorno
                    pdf.setStrokeColor(gray)
                    pdf.line( 25,y-2,295,y-2)
                    pdf.line(300,y-2,570,y-2)
                    
                    y -= 40
        pdf.showPage() # Chiude pagina 
    pdf.save() # Salva il PDF

# anno_input = int(input("Inserisci l'anno: "))
# genera_calendario_pdf(anno_input, output_file)


