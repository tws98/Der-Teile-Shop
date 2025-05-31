import tkinter as tk
from tkinter import ttk, messagebox

# Die Kunden-Klasse
class Kunden:
    def __init__(self, IDKunde, anrede, vorname, name, strasse, hausnummer, ort, PLZ, telefon, geburtsdatum, email, titel):
        self.IDKunde = IDKunde
        self.anrede = anrede
        self.vorname = vorname
        self.name = name
        self.strasse = strasse
        self.hausnummer = hausnummer
        self.ort = ort
        self.PLZ = PLZ
        self.telefon = telefon
        self.geburtsdatum = geburtsdatum
        self.email = email
        self.titel = titel

# Funktion zum Verwalten des Kunden
def kunden_verwalten(kunde, cur, conn):
    def daten_pruefen():
        # Werte aus der GUI holen
        anrede = entry_anrede.get()
        vorname = entry_vorname.get()
        name = entry_name.get()
        strasse = entry_strasse.get()
        hausnummer = entry_hausnummer.get()
        ort = entry_ort.get()
        plz = entry_plz.get()
        telefon = entry_telefon.get()
        geburtsdatum = entry_geburtsdatum.get()
        email = entry_email.get()
        titel = entry_titel.get()

        if not email:
            messagebox.showwarning("Hinweis", "Es wurde keine E-Mail-Adresse angegeben.")
        else:
            cur.execute("""SELECT kunden.IDKunde, anrede.Anrede, Vorname, Name, Straße, Hausnummer, ort.Ort, ort.PLZ, Telefon, Geburtsdatum, Email, Titel
FROM kunden INNER JOIN ort on ort.ID_Ort = kunden.OrtID
INNER JOIN anrede on anrede.ID_Anrede = kunden.Anrede
WHERE kunden.Vorname = ? AND kunden.Name = ? AND Straße = ? AND Hausnummer = ? AND PLZ = ? AND Ort = ?""",(vorname, name ,strasse, hausnummer, plz, ort))
            row = cur.fetchone()

            if row:
                kunde.IDKunde = row[0]
                messagebox.showinfo("Hinweis", "Ein Kunde mit diesen Adressdaten existiert bereits – aber ohne E-Mail.")
        
            else:
                kunde.IDKunde = None
                messagebox.showinfo("Keine Dublette", "Diese Kundendaten sind neu und können gespeichert werden.")

    def speichern():
        kunde.anrede = entry_anrede.get()
        kunde.vorname = entry_vorname.get()
        kunde.name = entry_name.get()
        kunde.strasse = entry_strasse.get()
        kunde.hausnummer = entry_hausnummer.get()
        kunde.ort = entry_ort.get()
        kunde.PLZ = entry_plz.get()
        kunde.telefon = entry_telefon.get()
        kunde.geburtsdatum = entry_geburtsdatum.get()
        kunde.email = entry_email.get()
        kunde.titel = entry_titel.get()

        # Ergebnis anzeigen
        label_result.config(text=f"{kunde.titel} {kunde.anrede} {kunde.vorname} {kunde.name}\n"
                                 f"{kunde.strasse} {kunde.hausnummer}, {kunde.PLZ} {kunde.ort}\n"
                                 f"Telefon: {kunde.telefon}, Geburtsdatum: {kunde.geburtsdatum}\n"
                                 f"E-Mail: {kunde.email}")
        try:
            # OrtID holen
            cur.execute("SELECT ID_Ort FROM ort WHERE Ort = ? AND PLZ = ?", (kunde.ort, kunde.PLZ))
            row = cur.fetchone()
            ortid = row[0] if row else None

            # AnredeID holen
            cur.execute("SELECT ID_Anrede FROM anrede WHERE Anrede = ?", (kunde.anrede,))
            row = cur.fetchone()
            anredeid = row[0] if row else None

            if ortid is None or anredeid is None:
                messagebox.showerror("Fehler", "Ungültige Anrede oder Ort/PLZ")
                return

            
            if kunde.IDKunde:  # UPDATE für vorhandene Kunden
                sql = """
                UPDATE kunden
                SET Anrede = ?, Vorname = ?, Name = ?, Straße = ?, Hausnummer = ?, OrtID = ?, 
                    Telefon = ?, Geburtsdatum = ?, Email = ?, Titel = ?
                WHERE IDKunde = ?;
            """
                werte = (
                anredeid, kunde.vorname, kunde.name, kunde.strasse, kunde.hausnummer,
                ortid, kunde.telefon, kunde.geburtsdatum, kunde.email, kunde.titel, kunde.IDKunde
                )
                cur.execute(sql, werte)

            else:  # INSERT für neue Kunden
                sql = """
                INSERT INTO kunden (Anrede, Vorname, Name, Straße, Hausnummer, OrtID, Telefon, 
                                    Geburtsdatum, Email, Titel)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
                werte = (
                anredeid, kunde.vorname, kunde.name, kunde.strasse, kunde.hausnummer,
                ortid, kunde.telefon, kunde.geburtsdatum, kunde.email, kunde.titel
                )
                cur.execute(sql, werte)

            conn.commit()
            messagebox.showinfo("Erfolg", "Änderungen wurden erfolgreich gespeichert.")
            root.destroy()

        except Exception as e:
            messagebox.showerror("Fehler beim Speichern", f"Ein Fehler ist aufgetreten:\n{str(e)}")
    
    
    # GUI erstellen
    root = tk.Tk()
    root.title("Kundenverwaltung")

    # Eingabefelder
    labels = ["Anrede", "Vorname", "Nachname", "Straße", "Hausnummer", "Ort", "PLZ", "Telefon", "Geburtsdatum", "E-Mail", "Titel"]
    eintraege = []
    daten = [kunde.anrede, kunde.vorname, kunde.name, kunde.strasse, kunde.hausnummer,
             kunde.ort, kunde.PLZ, kunde.telefon, kunde.geburtsdatum, kunde.email, kunde.titel]

    for i, (label, wert) in enumerate(zip(labels, daten)):
        ttk.Label(root, text=label + ":").grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry = ttk.Entry(root)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.insert(0, wert)
        eintraege.append(entry)

    # Einzelfelder den Variablen zuweisen
    (entry_anrede, entry_vorname, entry_name, entry_strasse, entry_hausnummer,
     entry_ort, entry_plz, entry_telefon, entry_geburtsdatum, entry_email, entry_titel) = eintraege

    # Prüfen-Button (nur wenn keine Kundendaten vorhanden)
    if not kunde.IDKunde:
        button_pruefen = ttk.Button(root, text="Daten prüfen", command=daten_pruefen)
        button_pruefen.grid(row=11, column=0, columnspan=2, pady=5)

    # Speichern-Button
    button_speichern = ttk.Button(root, text="Änderungen speichern", command=speichern)
    button_speichern.grid(row=12, column=0, columnspan=2, pady=10)

    # Ergebnis-Label
    label_result = ttk.Label(root, text=f"{kunde.titel} {kunde.anrede} {kunde.vorname} {kunde.name}\n"
                                        f"{kunde.strasse} {kunde.hausnummer}, {kunde.PLZ} {kunde.ort}\n"
                                        f"Telefon: {kunde.telefon}, Geburtsdatum: {kunde.geburtsdatum}\n"
                                        f"E-Mail: {kunde.email}")
    label_result.grid(row=13, column=0, columnspan=2, pady=20)
