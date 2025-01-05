#versione 24.2.19
# http://navigazione.altervista.org/python-fasi-lunari/
# Nanni Manca
# Carloforte, Sardegna
# email: nmanca@tiscali.it
# 
# dadosoft@virgilio.it Fidenza 01/2025
# tolto variabili globali e
# cambiato da procedure a funzioni che ritornato valori
# sembra che vada 

# Ernest William Brown

import math

class xval_rec:
    def __init__(self):
        self.OK = 0
        self.Code1 = 0
        self.Code2 = 0
# xval_rec
        
class data_rec:
    def __init__(self):
        self.JJD = 0.0
        self.Anno = 0
        self.Mese = 0
        self.Giorno = 0
        self.AnnoBis = 0
# data_rec

AryFasi = ['LN', 'PQ', 'LP', 'UQ'] 
# 0 LN Luna Nuova
# 1 PQ Primo Quarto
# 2 LP Luna Piena
# 3 UQ Ultimo Quarto
        

TPI = 2 *math.pi
RAD = math.pi /180

TABM = [0.041, 0.126, 0.203, 0.288, 0.370, 0.455,
        0.537, 0.622, 0.707, 0.789, 0.874, 0.956]

def Rmod(N, D):
    return N -Trunc(N /D) *D
# Rmod

def Trunc(X): 
    if X > 0.0:
        return math.floor(X)
    else:
        return math.ceil(X)
# Trunc()

def Frac(X): 
    return X -int(X)
# Frac()

def JJDateJ(Data):
    Z1= Data.JJD + 0.5
    Z= Trunc(Z1)
    A= Z
    B= A +1524
    C= Trunc((B -122.1) /365.25)
    D= Trunc(365.25 *C)
    E= Trunc((B -D) /30.6001)
    Data.JOUR= Trunc(B -D -Trunc(30.6001 *E))
    if E < 13.5:
        Data.MOIS= Trunc(E -1)
    else:
        Data.MOIS= Trunc(E -13)
    if Data.MOIS >= 3:
        Data.AN= Trunc(C -4716)
    else:
        Data.AN= Trunc(C -4715)
    return Data
# JJDateJ()

def JJDate(Data):
    Z1= Data.JJD + 0.5
    Z= Trunc(Z1)
    if Z < 2299161:
        A= Z
    else:
        ALPHA= Trunc((Z -1867216.25) /36524.25)
        A= Z +1 +ALPHA -Trunc(ALPHA /4)
    B= A +1524;
    C= Trunc((B -122.1) /365.25)
    D= Trunc(365.25 *C)
    E= Trunc((B -D) /30.6001)
    Data.Giorno= Trunc(B -D -Trunc(30.6001 *E))
    if (E<13.5):
        Data.Mese= Trunc(E -1)
    else:
        Data.Mese= Trunc(E -13)
    if (Data.Mese >= 3):
        Data.Anno= Trunc(C -4716)
    else:
        Data.Anno= Trunc(C -4715)
    return Data
# JJDate()

def BisG(Data):
    Data.AnnoBis= 0
    if (Data.Anno % 4 == 0):
        Data.AnnoBis= 1
    if (Data.Anno % 100 == 0) and (Data.Anno % 400 != 0):
        Data.AnnoBis= 0
    return Data
# BisG()

def BisJ(Data):
    if (Data.Anno % 4 == 0):
        Data.AnnoBis= 1
    else:
        Data.AnnoBis= 0
    return Data
# BisJ()

def CorrTetu(pMese,Data,xVal):
    D = xVal.Code1 /100.0 # TETU in secondi
    tetuS= 32.23 *(D -18.30) *(D -18.30) -15
    tetuJ= tetuS /86400.0
    # aggiunta di 30 secondi
    Data.JJD= Data.JJD +0.00034722222
    Data.JJD= Data.JJD -tetuJ
    if Data.JJD < 2299160.5:
        Data = JJDate(Data)
        Data = BisJ(Data)
    else:
        Data = JJDate(Data)
        Data = BisG(Data)
    xVal.OK = 0
    if Data.Mese == pMese:
        xVal.OK= 1
    return Data,xVal
# CorrTetu()

def GiorniDelMese(Data):
    ATabjm =[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if Data.JJD < 2299160.5:
        Data = BisJ(Data)
    else:
        Data = BisG(Data)
    if (Data.Mese == 2) and (Data.AnnoBis == 1):
        g= 29
    else:
        g= ATabjm[Data.Mese -1]
    return g
# GiorniDelMese

def VisaMoph(Fase,Data):
    # data e ora della fase 
    if Data.JJD < 2299160.5:
        Data = JJDateJ(Data)
    else:
        Data = JJDate(Data)
    # CET +1h -30 secondi (CorrTetu)
    Data.JJD= Data.JJD +1.0 /24.0 -1 /2880
    gg= Data.Giorno
    fracJ= Frac(Data.JJD +0.5) /1.0
    rh= fracJ *24.0
    hh= Trunc(rh)
    fracJ= rh -hh
    rm= fracJ *60
    mm= Trunc(rm)
    if hh == 24:
        ug= GiorniDelMese(Data)
        if Data.Giorno < ug:
            hh= 0
            gg= Data.Giorno +1
    if gg < 10: gg= ' ' +str(gg)
    key = f"{Data.Giorno:02d}-{Data.Mese:02d}"
    value = AryFasi[Fase]
    return key,value
# VisaMoph()

def MoonPh(Data):
    xVal = xval_rec()
    dMese={}
    xMese= Data.Mese;
    xVal.Code1= Data.Anno
    xVal.Code2= Data.Mese
    if (Data.Mese == 1):
        anno= Data.Anno -1
        Data.Mese= 12
    else:
        anno= Data.Anno
        Data.Mese= Data.Mese -1
    anno+= TABM[Data.Mese -1]
    k= (anno -1900) *12.3685
    lik= Trunc(k)
    rk= lik
    k= rk -0.25
    if(k < 0.0): k= k -1
    nx = 0
    for ii in range(12):
        k= k +0.25
        t= k /1236.85
        t2= t*t
        t3= t*t2
        j= (2415020.75933 + 29.5305888531*k
        + 0.0001337*t2 - 0.000000155*t3 
        + 0.00033*math.sin(RAD*(166.56 + 132.87*t - 0.009173*t2)))
        m= (RAD*(359.2242 + 29.10535608*k 
        - 0.0000333*t2 - 0.00000347*t3))
        m= m%(TPI)
        mp= (RAD*(306.0253 + 385.81691806*k
        + 0.0107306*t2 + 0.00001236*t3))
        mp= mp%(TPI)
        f= (RAD*(21.2964 + 390.67050646*k
        - 0.0016528*t2 - 0.00000239*t3))
        f= f%(TPI)
        xVal.OK = 0
        fase= ii%4
        # Correzione delle fasi
        if(fase==0) or (fase==2):
            # LN, LP
            j = (j + (0.1734 - 0.000393*t)*math.sin(m)
             + 0.0021*math.sin(2*m) - 0.4068*math.sin(mp)
             + 0.0161*math.sin(2*mp) - 0.0004*math.sin(3*mp)
             + 0.0104*math.sin(2*f) - 0.0051*math.sin(m+mp)
             - 0.0074*math.sin(m-mp) + 0.0004*math.sin(2*f+m)
             - 0.0004*math.sin(2*f-m) - 0.0006*math.sin(2*f+mp)
             + 0.0010*math.sin(2*f-mp) + 0.0005*math.sin(m+2*mp))
            Data.JJD= j
            Data,xVal = CorrTetu(xMese,Data,xVal)
            if (xVal.OK==1):
                key,value =VisaMoph(fase,Data)
                dMese[key] = value
        else:
            j= (j + (0.1721 - 0.0004*t)*math.sin(m)
             + 0.0021*math.sin(2*m) - 0.6280*math.sin(mp)
             + 0.0089*math.sin(2*mp) - 0.0004*math.sin(3*mp)
             + 0.0079*math.sin(2*f) - 0.0119*math.sin(m+mp)
             - 0.0047*math.sin(m-mp) + 0.0003*math.sin(2*f+m)
             - 0.0004*math.sin(2*f-m) - 0.0006*math.sin(2*f+mp)
             + 0.0021*math.sin(2*f-mp) + 0.0003*math.sin(m+2*mp)
             + 0.0004*math.sin(m-2*mp) - 0.0003*math.sin(2*m+mp))
            if (fase==1):
                # PQ
                Data.JJD = (j + 0.0028 - 0.0004*math.cos(m)
                           + 0.0003*math.cos(mp))
                Data,xVal = CorrTetu(xMese,Data,xVal)
                if(xVal.OK==1):
                    key,value =VisaMoph(fase,Data)
                    dMese[key] = value
            else: #fase=2
                # UQ
                Data.JJD = (j - 0.0028 + 0.0004*math.cos(m)
                           - 0.0003*math.cos(mp))
                Data,xVal = CorrTetu(xMese,Data,xVal)
                if(xVal.OK==1):
                    key,value =VisaMoph(fase,Data)
                    dMese[key] = value
    # for ii
    if (xVal.OK==1): nx= nx +1
    if (nx>=4 and xVal.OK==0): print('ERROR: break')
    Data.Anno= xVal.Code1
    Data.Mese= xVal.Code2
    return dMese
# MoonPh()

def FasiAnno(Anno): # da anno a 12 mesi
    dFasiLuna = {}
    Data = data_rec()
    if (Anno<-2500) or (Anno>2500):
        print("ERROR: Year out of range")
    else:
        for Mese in range(12): # (0.11)
            Data.Mese= Mese + 1
            Data.Anno= Anno
            dFasiLuna.update(MoonPh(Data))
        return dFasiLuna

'''
for anno in range(2024,2054):
    print(anno,FasiAnno(anno))
'''