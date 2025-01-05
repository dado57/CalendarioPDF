import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from calendarPdf import genera_pdf

def generate_pdf():
    year = int(year_var.get())
    include_moon = moon_phase_var.get()
    include_saints = saints_var.get()
    include_holidays = holidays_var.get()
    
    # Logica per generare il PDF del calendario
    options = []
    if include_moon:
        options.append("Fasi lunari")
    if include_saints:
        options.append("Santi")
    if include_holidays:
        options.append("Festivi")
    
    genera_pdf(year, fFL=include_moon, fSA=include_saints, fFE=include_holidays)
    
    messagebox.showinfo("Calendario PDF", f"Generazione PDF per l'anno {year} con opzioni: {', '.join(options)}")
    

# Creazione della finestra principale
root = tk.Tk()
root.title("DadoSoft - Calendario to PDF")
root.geometry("400x250")

# Etichetta del titolo
title_label = tk.Label(root, text="DadoSoft", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Frame per l'anno
frame_year = tk.Frame(root)
frame_year.pack(pady=5)

year_label = tk.Label(frame_year, text="Anno:")
year_label.pack(side=tk.LEFT, padx=5)

year_var = tk.StringVar(value="2025")
year_spinbox = ttk.Spinbox(frame_year, from_=1900, to=2100, textvariable=year_var, width=10)
year_spinbox.pack(side=tk.LEFT, padx=5)

# Checkbox per le opzioni
moon_phase_var = tk.BooleanVar(value=True)
saints_var = tk.BooleanVar(value=True)
holidays_var = tk.BooleanVar(value=True)

moon_phase_check = tk.Checkbutton(root, text="Fasi lunari", variable=moon_phase_var)
moon_phase_check.pack(anchor="w", padx=10)

saints_check = tk.Checkbutton(root, text="Santi", variable=saints_var)
saints_check.pack(anchor="w", padx=10)

holidays_check = tk.Checkbutton(root, text="Festivi", variable=holidays_var)
holidays_check.pack(anchor="w", padx=10)

# Pulsante per generare il PDF
generate_button = tk.Button(root, text="Crea PDF", command=generate_pdf)
generate_button.pack(pady=20)

# Avvio del ciclo principale
def on_closing():
    if messagebox.askokcancel("Uscita", "Vuoi davvero chiudere il programma?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
