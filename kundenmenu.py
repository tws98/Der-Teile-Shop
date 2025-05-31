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

# Funktion zum Erstellen der GUI und Speichern der Änderungen
def kunden_verwalten(kunde, cur, conn):
    # Funktion zum Speichern der Änderungen
    def speichern(cur, conn):
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
        
        # Anzeigen der gespeicherten Daten im Label
        label_result.config(text=f"{kunde.titel} {kunde.anrede} {kunde.vorname} {kunde.name}\n"
                                 f"{kunde.strasse} {kunde.hausnummer}, {kunde.PLZ} {kunde.ort}\n"
                                 f"Telefon: {kunde.telefon}, Geburtsdatum: {kunde.geburtsdatum}\n"
                                 f"E-Mail: {kunde.email}")
        

        #Für die neu gespeicherten Daten die Primary Keys holen
        try:
            # OrtID holen
            cur.execute("SELECT ID_Ort FROM ort WHERE Ort = ? AND PLZ = ?", (kunde.ort, kunde.PLZ))
            row = cur.fetchone()
            if row:
                ortid = row[0]

            else:
                None

            # AnredeID holen
            cur.execute("SELECT ID_Anrede FROM anrede WHERE Anrede = ?", (kunde.anrede,))
            row = cur.fetchone()
            if row:
                anredeid = row[0] 
                
            else:
                None

            if ortid is None or anredeid is None:
                messagebox.showerror("Fehler", "Ungültige Anrede oder Ort/PLZ")
                return

            # UPDATE-Statement
            sql = """
                UPDATE `kunden`
                SET `Anrede` = ?,
                    `Vorname` = ?,
                    `Name` = ?,
                    `Straße` = ?,
                    `Hausnummer` = ?,
                    `OrtID` = ?,
                    `Telefon` = ?,
                    `Email` = ?
                WHERE `IDKunde` = ?;
            """

            werte = (
                anredeid,
                kunde.vorname,
                kunde.name,
                kunde.strasse,
                kunde.hausnummer,
                ortid,
                kunde.telefon,
                kunde.email,
                kunde.IDKunde
            )

            cur.execute(sql, werte)
            conn.commit()
            messagebox.showinfo("Erfolg", "Änderungen gespeichert")
            root.destroy()

        except Exception as e:
            messagebox.showerror("Fehler beim Speichern", f"Ein Fehler ist aufgetreten:\n{str(e)}")

    # GUI erstellen
    root = tk.Tk()
    root.title("Kundenverwaltung")

    # Labels und Eingabefelder
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

    label_plz = ttk.Label(root, text="PLZ:")
    label_plz.grid(row=6, column=0, padx=10, pady=5, sticky="e")
    entry_plz = ttk.Entry(root)
    entry_plz.grid(row=6, column=1, padx=10, pady=5)
    entry_plz.insert(0, kunde.PLZ)

    label_telefon = ttk.Label(root, text="Telefon:")
    label_telefon.grid(row=7, column=0, padx=10, pady=5, sticky="e")
    entry_telefon = ttk.Entry(root)
    entry_telefon.grid(row=7, column=1, padx=10, pady=5)
    entry_telefon.insert(0, kunde.telefon)

    label_geburtsdatum = ttk.Label(root, text="Geburtsdatum:")
    label_geburtsdatum.grid(row=8, column=0, padx=10, pady=5, sticky="e")
    entry_geburtsdatum = ttk.Entry(root)
    entry_geburtsdatum.grid(row=8, column=1, padx=10, pady=5)
    entry_geburtsdatum.insert(0, kunde.geburtsdatum)

    label_email = ttk.Label(root, text="E-Mail:")
    label_email.grid(row=9, column=0, padx=10, pady=5, sticky="e")
    entry_email = ttk.Entry(root)
    entry_email.grid(row=9, column=1, padx=10, pady=5)
    entry_email.insert(0, kunde.email)

    label_titel = ttk.Label(root, text="Titel:")
    label_titel.grid(row=10, column=0, padx=10, pady=5, sticky="e")
    entry_titel = ttk.Entry(root)
    entry_titel.grid(row=10, column=1, padx=10, pady=5)
    entry_titel.insert(0, kunde.titel)

    # Button zum Speichern
    button_speichern = ttk.Button(root, text="Änderungen speichern", command=lambda: speichern(cur,conn))
    button_speichern.grid(row=11, column=0, columnspan=2, pady=20)

    # Ergebnisanzeige
    label_result = ttk.Label(root, text=f"{kunde.titel} {kunde.anrede} {kunde.vorname} {kunde.name}\n"
                                        f"{kunde.strasse} {kunde.hausnummer}, {kunde.PLZ} {kunde.ort}\n"
                                        f"Telefon: {kunde.telefon}, Geburtsdatum: {kunde.geburtsdatum}\n"
                                        f"E-Mail: {kunde.email}")
    label_result.grid(row=12, column=0, columnspan=2, pady=20)


