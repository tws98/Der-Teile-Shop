import tkinter as tk
from tkinter import ttk

# Die Kunden-Klasse
class Kunden:
    def __init__(self, anrede, vorname, name, strasse, hausnummer, ort, telefon, geburtsdatum, email, titel):
        self.anrede = anrede
        self.vorname = vorname
        self.name = name
        self.strasse = strasse
        self.hausnummer = hausnummer
        self.ort = ort
        self.telefon = telefon
        self.geburtsdatum = geburtsdatum
        self.email = email
        self.titel = titel

# Beispielkunde
kunde = Kunden('Herr', 'Max', 'Mustermann', 'Musterstraße', '12', 'Musterstadt', '0123456789', '01.01.1990', 'max@muster.de', 'Dr.')

# Funktion zum Erstellen der GUI und Speichern der Änderungen
def kunden_verwalten(kunde):
    # Funktion zum Speichern der Änderungen
    def speichern():
        kunde.anrede = entry_anrede.get()
        kunde.vorname = entry_vorname.get()
        kunde.name = entry_name.get()
        kunde.strasse = entry_strasse.get()
        kunde.hausnummer = entry_hausnummer.get()
        kunde.ort = entry_ort.get()
        kunde.telefon = entry_telefon.get()
        kunde.geburtsdatum = entry_geburtsdatum.get()
        kunde.email = entry_email.get()
        kunde.titel = entry_titel.get()
        
        # Anzeigen der gespeicherten Daten im Label
        label_result.config(text=f"{kunde.titel} {kunde.anrede} {kunde.vorname} {kunde.name}\n"
                                f"{kunde.strasse} {kunde.hausnummer}, {kunde.ort}\n"
                                f"Telefon: {kunde.telefon}, Geburtsdatum: {kunde.geburtsdatum}\n"
                                f"E-Mail: {kunde.email}")
    
    # GUI erstellen
    root = tk.Tk()
    root.title("Kundenverwaltung")

    # Labels und Eingabefelder für die GUI
    label_anrede = ttk.Label(root, text="Anrede:")
    label_anrede.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_anrede = ttk.Entry(root)
    entry_anrede.grid(row=0, column=1, padx=10, pady=5)
    entry_anrede.insert(0, kunde.anrede)

    label_vorname = ttk.Label(root, text="Vorname:")
    label_vorname.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_vorname = ttk.Entry(root)
    entry_vorname.grid(row=1, column=1, padx=10, pady=5)
    entry_vorname.insert(0, kunde.vorname)

    label_name = ttk.Label(root, text="Nachname:")
    label_name.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_name = ttk.Entry(root)
    entry_name.grid(row=2, column=1, padx=10, pady=5)
    entry_name.insert(0, kunde.name)

    label_strasse = ttk.Label(root, text="Straße:")
    label_strasse.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_strasse = ttk.Entry(root)
    entry_strasse.grid(row=3, column=1, padx=10, pady=5)
    entry_strasse.insert(0, kunde.strasse)

    label_hausnummer = ttk.Label(root, text="Hausnummer:")
    label_hausnummer.grid(row=4, column=0, padx=10, pady=5, sticky="e")
    entry_hausnummer = ttk.Entry(root)
    entry_hausnummer.grid(row=4, column=1, padx=10, pady=5)
    entry_hausnummer.insert(0, kunde.hausnummer)

    label_ort = ttk.Label(root, text="Ort:")
    label_ort.grid(row=5, column=0, padx=10, pady=5, sticky="e")
    entry_ort = ttk.Entry(root)
    entry_ort.grid(row=5, column=1, padx=10, pady=5)
    entry_ort.insert(0, kunde.ort)

    label_telefon = ttk.Label(root, text="Telefon:")
    label_telefon.grid(row=6, column=0, padx=10, pady=5, sticky="e")
    entry_telefon = ttk.Entry(root)
    entry_telefon.grid(row=6, column=1, padx=10, pady=5)
    entry_telefon.insert(0, kunde.telefon)

    label_geburtsdatum = ttk.Label(root, text="Geburtsdatum:")
    label_geburtsdatum.grid(row=7, column=0, padx=10, pady=5, sticky="e")
    entry_geburtsdatum = ttk.Entry(root)
    entry_geburtsdatum.grid(row=7, column=1, padx=10, pady=5)
    entry_geburtsdatum.insert(0, kunde.geburtsdatum)

    label_email = ttk.Label(root, text="E-Mail:")
    label_email.grid(row=8, column=0, padx=10, pady=5, sticky="e")
    entry_email = ttk.Entry(root)
    entry_email.grid(row=8, column=1, padx=10, pady=5)
    entry_email.insert(0, kunde.email)

    label_titel = ttk.Label(root, text="Titel:")
    label_titel.grid(row=9, column=0, padx=10, pady=5, sticky="e")
    entry_titel = ttk.Entry(root)
    entry_titel.grid(row=9, column=1, padx=10, pady=5)
    entry_titel.insert(0, kunde.titel)

    # Button zum Speichern der Änderungen
    button_speichern = ttk.Button(root, text="Änderungen speichern", command=speichern)
    button_speichern.grid(row=10, column=0, columnspan=2, pady=20)

    # Label, um die aktuellen Daten anzuzeigen
    label_result = ttk.Label(root, text=f"{kunde.titel} {kunde.anrede} {kunde.vorname} {kunde.name}\n"
                                       f"{kunde.strasse} {kunde.hausnummer}, {kunde.ort}\n"
                                       f"Telefon: {kunde.telefon}, Geburtsdatum: {kunde.geburtsdatum}\n"
                                       f"E-Mail: {kunde.email}")
    label_result.grid(row=11, column=0, columnspan=2, pady=20)
