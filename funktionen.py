import customtkinter as ctk
from tkinter import messagebox
import bcrypt
import kundenmenu
import funktion_auftragserfassung
import funktionen_lagerbestand

# Klasse für die Kundendaten aus der Datenbank
class Kunden():
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

# Klasse für die GUI-Elemente
class Eingabe:
    def __init__(self, parent):
        self.entry_email = None
        self.entry_benutzer = ""
        self.entry_passwort = None
        self.entry_passwort_wdh = None
        self.login_email = None
        self.login_passwort = None
        self.id = None
        self.benutzername = None
        self.rolle = None
        self.kunden_id = None
        self.passworthash = None
        self.cur = None
        self.parent = parent
        self.frame = ctk.CTkFrame(self.parent)
        self.conn = None

    def clear_window(self, window):
        #Funktion um alle GUI Einträge zu löschen und nur das root zu behalten
        for widget in window.winfo_children():
            widget.destroy()

    def registrierung_ui(self, parent, cur, conn):
        parent.title("Benutzer Registrierung")
        # globaler Container
        self.frame = ctk.CTkFrame(parent)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        # Widgets der GUI Anmeldung
        ctk.CTkLabel(self.frame, text="Benutzer Registrierung", font=("Arial", 12, "bold")).pack(pady=10)
        ctk.CTkLabel(self.frame, text="E-Mail:").pack()
        self.entry_email = ctk.CTkEntry(self.frame)
        self.entry_email.pack(pady=5)

        ctk.CTkLabel(self.frame, text="Passwort:").pack()
        self.entry_passwort = ctk.CTkEntry(self.frame, show="*")
        self.entry_passwort.pack(pady=5)

        ctk.CTkLabel(self.frame, text="Passwort wiederholen:").pack()
        self.entry_passwort_wdh = ctk.CTkEntry(self.frame, show="*")
        self.entry_passwort_wdh.pack(pady=5)

        ctk.CTkButton(self.frame, text="Registrieren", command=lambda: self.registrieren(cur, conn)).pack(pady=10)
        ctk.CTkButton(self.frame, text="Beenden", command=self.beenden).pack(pady=10)

    def anmeldung_ui(self, parent, cur, conn):
        #globaler container
        self.frame = ctk.CTkFrame(parent)
        self.frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")

        # Widgets der GUI Anmeldung
        ctk.CTkLabel(self.frame, text="Benutzer Anmeldung", font=("Arial", 12, "bold")).pack(pady=10)
        ctk.CTkLabel(self.frame, text="E-Mail:").pack()
        self.login_email = ctk.CTkEntry(self.frame)
        self.login_email.pack(pady=5)

        ctk.CTkLabel(self.frame, text="Passwort:").pack()
        self.login_passwort = ctk.CTkEntry(self.frame, show="*")
        self.login_passwort.pack(pady=5)

        ctk.CTkButton(self.frame, text="Anmelden", command=lambda: self.anmelden(cur, conn)).pack(pady=10)

    def beenden(self):
        # Beenden Button
        self.frame.destroy()
        self.parent.destroy()

    def registrieren(self, cur, conn):
        # entrys der gui holen
        email = self.entry_email.get()
        pw1 = self.entry_passwort.get()
        pw2 = self.entry_passwort_wdh.get()

        if "@" not in email:
            #überprüfung das eine Email angegeben wird
            messagebox.showwarning("Fehler", "Bitte geben Sie eine gültige E-Mail - Adresse ein.")
            return

        #überprüfung, dass die Felder ausgefüllt sind
        if not email or not pw1 or not pw2:
            messagebox.showwarning("Fehler", "Bitte alle Felder ausfüllen.")
            return

        #Überprüfung, dass die passwörter gleich sind
        if pw1 != pw2:
            messagebox.showerror("Fehler", "Passwörter stimmen nicht überein.")
            return

        #passwort hashen
        hashed = bcrypt.hashpw(pw1.encode(), bcrypt.gensalt())

        #Benutzerdaten in Datenbank speichern
        try:
            cur.execute("INSERT INTO benutzer (benutzername, passwort_hash, rolle) VALUES (?, ?, ?)", (email, hashed.decode(), "kunde"))
            conn.commit()
            #neu angelegte benutzer-id aus Datenbank holen um sie unten zu verknüpfen
            cur.execute("SELECT benutzer.id FROM benutzer WHERE benutzer.benutzername = ?", (email,))
            row = cur.fetchone()
            idbenutzer = row[0]
            #überprüfung ob Kundendaten bereits angelegt sind:
            cur.execute("SELECT kunden.Email FROM kunden WHERE kunden.Email = ?", (email,))
            row = cur.fetchone()
            mail = row[0] if row else None

             # Falls e-mail in Datenbank (Kunden) bereits hinterlegt ist, KundenID mit Benutzer Tabelle verknüpfen
            if mail == email:
                cur.execute("SELECT kunden.IDKunde FROM kunden WHERE kunden.Email = ?", (mail,))
                row = cur.fetchone()
                idkunde = row[0]
                cur.execute("UPDATE `benutzer` SET `kunden_id` = ? WHERE `benutzer`.`id` = ?", (idkunde, idbenutzer))
                conn.commit()
                messagebox.showinfo("Erfolg", "Registrierung erfolgreich.")

            # Falls keine E-Mail hinterlegt ist, dann soll das Kundenmenü direkt aufgerufen werden zum Daten eintragen
            else:
                messagebox.showwarning("Erfolg.", "Der Benutzer wurde erfolgreich registriert.\n Bitte tragen Sie Ihre Daten auf der Folgeseite ein.")
                self.clear_window(self.parent)
                menu = Eingabe(self.parent)
                menu.kunden_menu(self.parent, email, cur, conn)

        except Exception as e:
            messagebox.showerror("Fehler", f"Registrierung fehlgeschlagen: {e}")
            # Eingaben der Datenbank zurücksetzen, sobald ein Fehler auftritt
            conn.rollback()

    def hauptmenu_admin(self, parent, cur, conn):
        #hauptmenü des Inhabers nach der Anmeldung
        parent.title("Hauptmenü")
        self.frame.destroy()
        self.frame = ctk.CTkFrame(parent)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        # Einzelne Buttons für das Hauptmenü
        ctk.CTkLabel(self.frame, text="Hauptmenü", font=("Arial", 12, "bold")).pack(pady=10)
        ctk.CTkButton(self.frame, text="Kundenübersicht", command=lambda: self.kunden_übersicht(cur, conn)).pack(pady=10, padx=20)
        ctk.CTkButton(self.frame, text="Auftragserfassung öffnen", command=lambda: funktion_auftragserfassung.starte_auftrag_gui(parent,cur, conn)).pack(pady=15,padx=20)
        ctk.CTkButton(self.frame, text="Lagerverwaltung", command=lambda: funktionen_lagerbestand.starte_produkt_gui(parent,cur,conn)).pack(pady=20, padx=20)
        ctk.CTkButton(self.frame, text="Ausloggen", command=lambda: self.logout(conn)).pack(pady=25, padx=20)

    def kunden_menu(self, parent, email, cur, conn):
        #hauptmenü für Kunden
        parent.title("Kundenmenü")
        self.frame = ctk.CTkFrame(parent)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="n")
        ctk.CTkLabel(self.frame, text="Kundenmenü", font=("Arial", 12, "bold")).pack(pady=10)

        # Daten aus der Kunden-Datenbank abrufen
        cur.execute("""SELECT kunden.IDKunde, anrede.Anrede, Vorname, Name, Straße, Hausnummer, ort.Ort, ort.PLZ, Telefon, Geburtsdatum, Email, Titel
                        FROM kunden 
                        INNER JOIN ort ON ort.ID_Ort = kunden.OrtID
                        INNER JOIN anrede ON anrede.ID_Anrede = kunden.Anrede
                        WHERE kunden.Email = ?""", (email,))
        row = cur.fetchone()

        if not row:
            # Leere Werte übergeben, wenn kein Kunde gefunden wurde
            adresse = Kunden(
                "",  # IDKunde
                "",  # Anrede
                "",  # Vorname
                "",  # Name
                "",  # Straße
                "",  # Hausnummer
                "",  # Ort
                "",  # PLZ
                "",  # Telefon
                "",  # Geburtsdatum
                email,  # Email
                ""   # Titel
            )
        else:
            # Daten vorhanden → Kundenobjekt erstellen
            adresse = Kunden(*row)# Nimm alle Elemente aus row und übergib sie einzeln als Argumente an die Funktion/Klasse.

        # Buttons anzeigen
        ctk.CTkButton(self.frame, text="Adressdaten anzeigen", command=lambda: kundenmenu.kunden_verwalten(adresse, cur, conn)).pack(pady=30, padx=20)
        ctk.CTkButton(self.frame, text="Ausloggen", command=lambda: self.logout(conn)).pack(pady=40, padx=20)

    # logout Funktion (zurück in die Benutzeranmeldung - Datenbankverbindung bleibt aktiv)
    def logout(self, conn):
        self.clear_window(self.parent)
        self.conn = conn

        if not self.conn:
            messagebox.showerror("Fehler", "Datenbankverbindung ist nicht mehr aktiv.")
            return

        # Um die Datenbankverbindung aufrecht zu erhalten
        import datenbankverbindung
        datenbank = datenbankverbindung.Datenbank(self.parent)
        datenbank.conn = self.conn
        datenbank.connected = True
        datenbank.zeige_benutzer_login()

    # Funktion für die Kundenübersicht
    def kunden_übersicht(self, cur, conn):
        self.frame.destroy()
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        # Überschrift
        ctk.CTkLabel(self.frame, text="Kundenübersicht", font=("Arial", 14, "bold")).pack(pady=5)

        # Suchfeld für Nachnamen
        such_frame = ctk.CTkFrame(self.frame)
        such_frame.pack(pady=5)

        ctk.CTkLabel(such_frame, text="Nachname:").pack(side="left")
        entry_suche = ctk.CTkEntry(such_frame)
        entry_suche.pack(side="left", padx=5)

        def daten_anzeigen(nachname_filter=None): # Optionaler Wert zum übergeben
            # Textbox leeren
            self.text_box.configure(state="normal")
            self.text_box.delete("1.0", "end")

            if nachname_filter:  # Wird ein Wert übergeben, dann soll nach dem nachname_filter gesucht werden
                cur.execute("""SELECT kunden.IDKunde, anrede.Anrede, Vorname, Name, Straße, Hausnummer, ort.PLZ, ort.Ort, Telefon, Geburtsdatum, Email, Titel
                            FROM kunden
                            INNER JOIN ort ON ort.ID_Ort = kunden.OrtID
                            INNER JOIN anrede ON anrede.ID_Anrede = kunden.Anrede
                            WHERE Name LIKE ?
                            GROUP BY IDKunde""", (f"%{nachname_filter}%",))
            else: # Wird kein Parameter übergeben, dann sollen alle Kunden aufgelistet werden
                cur.execute("""SELECT kunden.IDKunde, anrede.Anrede, Vorname, Name, Straße, Hausnummer, ort.PLZ, ort.Ort, Telefon, Geburtsdatum, Email, Titel
                            FROM kunden
                            INNER JOIN ort ON ort.ID_Ort = kunden.OrtID
                            INNER JOIN anrede ON anrede.ID_Anrede = kunden.Anrede
                            GROUP BY IDKunde""")

            kunden = cur.fetchall() # Alle SQL Abfrage-Daten in die Variable speichern
            if not kunden: # Überprüfung ob SQL-Abfrage ein Ergebnis liefert
                self.text_box.insert("end", "Keine Kunden gefunden.")
            else:
                for k in kunden:
                    eintrag = (f"{k[11]} {k[1]} {k[2]} {k[3]}\n"
                               f"{k[4]} {k[5]}, {k[6]} {k[7]}\n"
                               f"Tel: {k[8]} | Geburtsdatum: {k[9]}\n"
                               f"E-Mail: {k[10]}\n{'-'*40}\n") # -- für Zeilenumbruch / Trennung
                    self.text_box.insert("end", eintrag) # in die Textbox einfügen

            self.text_box.configure(state="disabled") # Textbox schreibgeschützt

        def suche_ausführen():
            nachname = entry_suche.get().strip()
            daten_anzeigen(nachname)

        ctk.CTkButton(such_frame, text="Suchen", command=suche_ausführen).pack(side="left", padx=5)
        ctk.CTkButton(such_frame, text="Zurück", command=lambda: self.hauptmenu_admin(self.parent, cur, conn)).pack(side="left", padx=10)

        # Scrollbare Textbox
        text_frame = ctk.CTkFrame(self.frame)
        text_frame.pack(fill="both", expand=True)

        self.text_box = ctk.CTkTextbox(text_frame, height=200, width=80, wrap="word")
        self.text_box.pack(side="left", fill="both", expand=True)

    # def auftragseingang(self):
    #     self.frame.destroy()

    # def lagerverwaltung(self):
    #     self.frame.destroy()

    def anmelden(self, cur, conn):
        # daten aus entrys der GUI holen
        email = self.login_email.get()
        pw = self.login_passwort.get()
        self.conn = conn

        if not email or not pw:
             # Überprüfung, dass alle Textboxen ausgefüllt sind
            messagebox.showwarning("Fehler", "Bitte alle Felder ausfüllen.")
            return

        try:
            # benutzername (Email) aus der Datenbank holen
            cur.execute("SELECT benutzername FROM benutzer WHERE benutzername = ?", (email,))
            benutzername = cur.fetchone()
            # gehashtes Passwort aus der Datenbank holen
            cur.execute("SELECT benutzer.passwort_hash FROM benutzer WHERE benutzer.benutzername = ?",(benutzername[0],))
            # hier muss [0] rein, weil die variable ein Tuple aus der Datenbank ist
            row = cur.fetchone()
            passworthash = row[0] #<-- nötig damit der Tuple zu einem einzelnen String zum vergleichen wird
            if bcrypt.checkpw(pw.encode(), passworthash.encode()):
                # überprüfung ob passwort gleich ist
                passwort = True

            else:
                messagebox.showerror("Fehler", f"Passwort stimmt nicht überein!")
                print ("Passwort stimmt nicht überein!")


            if not benutzername:
                messagebox.showerror("Fehler", "Benutzername nicht gefunden.")

            if passwort and benutzername:
                # Wenn beides übereinstimmt soll Benutzer angemeldet werden
                messagebox.showinfo("Hinweis", f"Anmeldung für {email} erfolgreich.")
                self.clear_window(self.parent)
                menu = Eingabe(self.parent)
                cur.execute("SELECT benutzer.rolle FROM benutzer WHERE benutzer.benutzername = ?",(benutzername[0],))
                row = cur.fetchone()
                rolle = row[0]

                # Überprüfung ob Admin oder Kunde sich anmeldet
                if rolle == "inhaber":
                    menu.hauptmenu_admin(self.parent,cur,conn)

                elif rolle == "kunde":
                    menu.kunden_menu(self.parent,email,cur,conn)
                 


        except Exception as e:
            messagebox.showerror("Fehler", f"Anmeldung fehlgeschlagen: {e}")
            print (e)