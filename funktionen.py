import tkinter as tk
from tkinter import ttk, messagebox
import bcrypt
import kundenmenu
import datenbankverbindung

class Kunden():
    def __init__(self,IDKunde, anrede,vorname,name,strasse,hausnummer,ort,PLZ,telefon,geburtsdatum,email,titel):
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

class Eingabe:
    def __init__(self,parent):
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
        self.frame = ttk.Frame(self.parent)
        self.conn = None


    def clear_window(self,window):
        #Funktion um alle GUI Einträge zu löschen und nur das root zu behalten
        for widget in window.winfo_children():
            widget.destroy()

    def registrierung_ui(self,parent, cur,conn):
        # globaler Container
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        ttk.Label(self.frame, text="Benutzer Registrierung", font=("Arial", 12, "bold")).pack(pady=10)

        ttk.Label(self.frame, text="E-Mail:").pack()
        self.entry_email = ttk.Entry(self.frame)
        self.entry_email.pack(pady=5)

        ttk.Label(self.frame, text="Passwort:").pack()
        self.entry_passwort = ttk.Entry(self.frame, show="*")
        self.entry_passwort.pack(pady=5)

        ttk.Label(self.frame, text="Passwort wiederholen:").pack()
        self.entry_passwort_wdh = ttk.Entry(self.frame, show="*")
        self.entry_passwort_wdh.pack(pady=5)

        ttk.Button(self.frame, text="Registrieren", command=lambda: self.registrieren(cur,conn)).pack(pady=10)



    def anmeldung_ui(self, parent, cur, conn):
        #globaler container
        self.frame = ttk.Frame(parent) 
        self.frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")

        ttk.Label(self.frame, text="Benutzer Anmeldung", font=("Arial", 12, "bold")).pack(pady=10)

        ttk.Label(self.frame, text="E-Mail:").pack()
        self.login_email = ttk.Entry(self.frame)
        self.login_email.pack(pady=5)

        ttk.Label(self.frame, text="Passwort:").pack()
        self.login_passwort = ttk.Entry(self.frame, show="*")
        self.login_passwort.pack(pady=5)

        ttk.Button(self.frame, text="Anmelden", command=lambda: self.anmelden(cur,conn)).pack(pady=10)


    def registrieren(self, cur, conn):
        # entrys der gui holen
        email = self.entry_email.get()
        pw1 = self.entry_passwort.get()
        pw2 = self.entry_passwort_wdh.get()

        if not "@" in email:
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
            cur.execute(
            "INSERT INTO benutzer (benutzername, passwort_hash, rolle) VALUES (?, ?, ?)",
            (email, hashed.decode(), "kunde")
        )
            conn.commit()
            messagebox.showinfo("Erfolg", "Registrierung erfolgreich!")
            #neu angelegte benutzer-id aus Datenbank holen um sie unten zu verknüpfen
            cur.execute("SELECT benutzer.id FROM benutzer WHERE benutzer.benutzername = ?",(email,))#<-- Komma um ein Tuple zu übergeben
            row = cur.fetchone()
            idbenutzer = row[0]
            #überprüfung ob Kundendaten bereits angelegt sind:
            cur.execute("SELECT kunden.Email FROM kunden WHERE kunden.Email = ?",(email,))
            row = cur.fetchone()
            mail = row[0]
            if mail == email:
                cur.execute("SELECT kunden.IDKunde FROM kunden WHERE kunden.Email = ?",(mail,))
                row = cur.fetchone()
                idkunde = row [0]
                cur.execute(f"UPDATE `benutzer` SET `kunden_id` = '{idkunde}' WHERE `benutzer`.`id` = {idbenutzer};" )
                conn.commit()


        
        except Exception as e:
            messagebox.showerror("Fehler", f"Registrierung fehlgeschlagen: {e}")
            # Eingaben der Datenbank zurücksetzen, sobald ein Fehler auftritt
            conn.rollback()



    def hauptmenu_admin (self,parent):
        #hauptmenü des Inhabers nach der Anmeldung
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0,column=0,padx=20, pady=20, sticky="n")
        ttk.Label(self.frame, text="Hauptmenü",font=("Arial", 12, "bold")).pack(pady=10)

 
        ttk.Button(self.frame, text="Kundenübersicht", command=self.kunden_übersicht).pack(pady=10,padx=20)
        ttk.Button(self.frame, text="Auftragseingabe", command=self.auftragseingang).pack(pady=20,padx=20)
        ttk.Button(self.frame, text="Lagerverwaltung", command=self.lagerverwaltung).pack(pady=30,padx=20)
        ttk.Button(self.frame, text="Ausloggen", command=self.logout).pack(pady=40,padx=20)


    def kunden_menu(self, parent, email,cur,conn):

        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0,column=0,padx=20, pady=20, sticky="n")
        ttk.Label(self.frame, text="Kundenmenü",font=("Arial", 12, "bold")).pack(pady=10)
       

        cur.execute ("""SELECT kunden.IDKunde, anrede.Anrede, Vorname, Name, Straße, Hausnummer, ort.Ort, ort.PLZ, Telefon, Geburtsdatum, Email, Titel
FROM kunden INNER JOIN ort on ort.ID_Ort = kunden.OrtID
INNER JOIN anrede on anrede.ID_Anrede = kunden.Anrede
WHERE kunden.Email = ?""",(email,))
        row = cur.fetchone()
        adresse = Kunden(*row)
        ttk.Button(self.frame, text="Adressdaten anzeigen", command=lambda: kundenmenu.kunden_verwalten(adresse,cur,conn)).pack(pady=30,padx=20)
        ttk.Button(self.frame, text="Ausloggen", command=lambda: self.logout(parent)).pack(pady=40,padx=20)


    
    # einzelne Funktionen für die Hauptmenü buttons
    def logout(self,parent):
        self.frame.destroy()
        instanz = datenbankverbindung.Datenbank(parent)
        instanz.datenbankverbindung.Datenbank(self.benutzername,self.passwort)

    def kunden_übersicht(self,cur):
        self.frame.destroy()
        cur.execute("""SELECT kunden.IDKunde,anrede.Anrede, Vorname, Name, Straße, Hausnummer, ort.Ort, Telefon, Geburtsdatum, Email, Titel
FROM kunden INNER JOIN ort on ort.ID_Ort = kunden.OrtID
INNER JOIN anrede on anrede.ID_Anrede = kunden.Anrede""")

    def auftragseingang(self):
        self.frame.destroy()

    def lagerverwaltung(self):
        self.frame.destroy()



    def anmelden(self,cur,conn):
        # daten aus entrys der GUI holen
        email = self.login_email.get()
        pw = self.login_passwort.get()

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
                print ("Passwort stimmt überein!")
                passwort = True

            else:
                messagebox.showerror("Fehler", f"Passwort stimmt nicht überein!")
                print ("Passwort stimmt nicht überein!")


            if benutzername:
                print("Benutzername stimmt überein!")
                # Check Reasons (nicht notwendig)

            else:
                messagebox.showerror("Fehler", "Benutzername nicht gefunden.")

            if passwort and benutzername:
                # Wenn beides übereinstimmt soll Benutzer angemeldet werden
                messagebox.showinfo("Hinweis", f"Anmeldung für {email} erfolgreich.")
                self.clear_window(self.parent)
                menu = Eingabe(self.parent)
                cur.execute("SELECT benutzer.rolle FROM benutzer WHERE benutzer.benutzername = ?",(benutzername[0],))
                row = cur.fetchone()
                rolle = row[0]

                if rolle == "inhaber":
                    menu.hauptmenu_admin(self.parent)

                elif rolle == "kunde":
                    menu.kunden_menu(self.parent,email,cur,conn)

                #else:
                #print("Fehler in der Datenbank. Bitte Datenbank überprüfen!")
                    


        except Exception as e:
            messagebox.showerror("Fehler", f"Anmeldung fehlgeschlagen: {e}")
            print (e)


