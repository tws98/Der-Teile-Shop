import tkinter as tk
from tkinter import ttk, messagebox

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

        #Überprüfung ob Email übereinstimmt
        if not email or kunde.email != email:
            messagebox.showwarning("Hinweis", "Die E-Mail stimmt nicht überein.")
            return

        
        cur.execute("""
            SELECT kunden.IDKunde FROM kunden
            INNER JOIN ort ON ort.ID_Ort = kunden.OrtID
            INNER JOIN anrede ON anrede.ID_Anrede = kunden.Anrede
            WHERE kunden.Vorname = ? AND kunden.Name = ? AND Straße = ? AND Hausnummer = ? AND PLZ = ? AND Ort = ? AND Geburtsdatum = ?
        """, (vorname, name, strasse, hausnummer, plz, ort, geburtsdatum))
        row = cur.fetchone()

        #Überprüfung ob eingegebene Daten bereits vorhanden sind
        if row:
            kunde.IDKunde = row[0]
            messagebox.showinfo("Hinweis", "Ein Kunde mit diesen Adressdaten existiert bereits – aber ohne E-Mail.")
        else:
            kunde.IDKunde = None
            messagebox.showinfo("Keine Dublette", "Diese Kundendaten sind neu und können gespeichert werden.")

    # Funktion zum speichern / aktualisieren der Kundendaten
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

        # Ort und PLZ überprüfen ob, sie hinterlegt ist
        try:
            cur.execute("SELECT ID_Ort FROM ort WHERE Ort = ? AND PLZ = ?", (kunde.ort, kunde.PLZ))
            row = cur.fetchone()
            if row:
                ortid = row[0]

            else:
                None

        # Überprüfung ob richtige Anrede ausgewählt wurde
            cur.execute("SELECT ID_Anrede FROM anrede WHERE Anrede = ?", (kunde.anrede,))
            row = cur.fetchone()

            if row:
                anredeid = row[0]

            else:
                None

            if ortid is None or anredeid is None:
                messagebox.showerror("Fehler", "Ungültige Anrede oder Ort/PLZ")
                return

            # Falls Kunde hinterlegt ist, dann 'Update' in SQL um die neuen Daten zu speichern
            if kunde.IDKunde:
                cur.execute("""
                    UPDATE kunden
                    SET Anrede=?, Vorname=?, Name=?, Straße=?, Hausnummer=?, OrtID=?, Telefon=?, Geburtsdatum=?, Email=?, Titel=?
                    WHERE IDKunde=?
                """, (anredeid, kunde.vorname, kunde.name, kunde.strasse, kunde.hausnummer,
                       ortid, kunde.telefon, kunde.geburtsdatum, kunde.email, kunde.titel, kunde.IDKunde))
                
            # Falls Kunde nicht hinterlegt ist, dann Insert SQL-Befehl um neue Daten anzulegen
            else:
                cur.execute("""
                    INSERT INTO kunden (Anrede, Vorname, Name, Straße, Hausnummer, OrtID, Telefon, Geburtsdatum, Email, Titel)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (anredeid, kunde.vorname, kunde.name, kunde.strasse, kunde.hausnummer,
                       ortid, kunde.telefon, kunde.geburtsdatum, kunde.email, kunde.titel))

            conn.commit()

            # Kunden ID und Benutzer ID aus Datenbank holen um diese miteinander zu Verknüpfen
            cur.execute("SELECT kunden.IDKunde FROM kunden WHERE kunden.Email = ?", (kunde.email,))
            idkunde = cur.fetchone()[0]
            cur.execute("SELECT benutzer.id FROM benutzer WHERE benutzer.benutzername = ?", (kunde.email,))
            idbenutzer = cur.fetchone()[0]

            # Verknüpfung der ids in der Tabelle Benutzer
            if idkunde and idbenutzer:
                cur.execute("UPDATE `benutzer` SET `kunden_id` = ? WHERE `benutzer`.`id` = ?", (idkunde, idbenutzer))
                conn.commit()
                messagebox.showinfo("Erfolg", "Änderungen wurden erfolgreich gespeichert.")
                root.destroy()
            else:
                messagebox.showerror("Fehler", "Kunde oder Benutzer nicht gefunden.")

        except Exception as e:
            messagebox.showerror("Fehler beim Speichern", f"Ein Fehler ist aufgetreten:\n{str(e)}")
            conn.rollback()

    # Neues Root Fenster für die Kundendaten
    root = tk.Tk()
    root.title("Kundendaten verwalten")

    labels = ["Anrede", "Vorname", "Nachname", "Straße", "Hausnummer", "Ort", "PLZ",
              "Telefon", "Geburtsdatum", "E-Mail", "Titel"]
    daten = [kunde.anrede, kunde.vorname, kunde.name, kunde.strasse, kunde.hausnummer,
             kunde.ort, kunde.PLZ, kunde.telefon, kunde.geburtsdatum, kunde.email, kunde.titel]

    eintraege = []

    # Einzelne Entrys und Labels erstellen
    for i, (label, wert) in enumerate(zip(labels, daten)):
        ttk.Label(root, text=label + ":").grid(row=i, column=0, padx=10, pady=5, sticky="e")

        entry = ttk.Entry(root)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.insert(0, wert)

        # Email Label/Entry auf 'readonly' setzen um, Redundanz zu vermeiden
        if label == "E-Mail":
            entry.config(state="readonly")

        # Falls Daten bereits vorhanden, werden sie hierdurch direkt angezeigt
        eintraege.append(entry)

    (entry_anrede, entry_vorname, entry_name, entry_strasse, entry_hausnummer,
     entry_ort, entry_plz, entry_telefon, entry_geburtsdatum, entry_email, entry_titel) = eintraege

    # Button 'Daten prüfen' nur anzeigen, wenn kein Kunde hinterlegt ist
    if not kunde.IDKunde:
        ttk.Button(root, text="Daten prüfen", command=daten_pruefen).grid(row=11, column=0, columnspan=2, pady=5)

    # Speichern Button
    ttk.Button(root, text="Änderungen speichern", command=speichern).grid(row=12, column=0, columnspan=2, pady=10)

    # Änderungen/Ergebnisse unten anzeigen
    label_result = ttk.Label(root, text=f"{kunde.titel} {kunde.anrede} {kunde.vorname} {kunde.name}\n"
                                        f"{kunde.strasse} {kunde.hausnummer}, {kunde.PLZ} {kunde.ort}\n"
                                        f"Tel: {kunde.telefon}, Geburtsdatum: {kunde.geburtsdatum}\n"
                                        f"E-Mail: {kunde.email}")
    label_result.grid(row=13, column=0, columnspan=2, pady=20)
