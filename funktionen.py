import tkinter as tk
from tkinter import ttk, messagebox
import bcrypt


class Eingabe:
    def __init__(self,parent):
        self.entry_email = None
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


    def registrierung_ui(self,cur,conn):
        frame = self.frame
        frame.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        ttk.Label(frame, text="Benutzer Registrierung", font=("Arial", 12, "bold")).pack(pady=10)

        ttk.Label(frame, text="E-Mail:").pack()
        self.entry_email = ttk.Entry(frame)
        self.entry_email.pack(pady=5)

        ttk.Label(frame, text="Passwort:").pack()
        self.entry_passwort = ttk.Entry(frame, show="*")
        self.entry_passwort.pack(pady=5)

        ttk.Label(frame, text="Passwort wiederholen:").pack()
        self.entry_passwort_wdh = ttk.Entry(frame, show="*")
        self.entry_passwort_wdh.pack(pady=5)

        ttk.Button(frame, text="Registrieren", command=lambda: self.registrieren(cur,conn)).pack(pady=10)



    def anmeldung_ui(self, parent, cur, conn):
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")

        ttk.Label(frame, text="Benutzer Anmeldung", font=("Arial", 12, "bold")).pack(pady=10)

        ttk.Label(frame, text="E-Mail:").pack()
        self.login_email = ttk.Entry(frame)
        self.login_email.pack(pady=5)

        ttk.Label(frame, text="Passwort:").pack()
        self.login_passwort = ttk.Entry(frame, show="*")
        self.login_passwort.pack(pady=5)

        ttk.Button(frame, text="Anmelden", command=lambda: self.anmelden(cur,conn)).pack(pady=10)


    def registrieren(self, cur, conn):
        # entrys der gui holen
        email = self.entry_email.get()
        pw1 = self.entry_passwort.get()
        pw2 = self.entry_passwort_wdh.get()

        if not "@" in email:
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
        
        except Exception as e:
            #if "Duplicate" in e:
             #   messagebox.showerror("Fehler",f"Die E-Mail Adresse {email} ist bereits vergeben.")
            messagebox.showerror("Fehler", f"Registrierung fehlgeschlagen: {e}")
            # Eingaben der Datenbank zurücksetzen, sobald ein Fehler auftritt
            conn.rollback()

        print (hashed)


    def anmelden(self,cur,conn):
        # daten aus entrys der GUI holen
        email = self.login_email.get()
        pw = self.login_passwort.get()

        if not email or not pw:
            # Überprüfung, dass alle Textboxen ausgefüllt sind
            messagebox.showwarning("Fehler", "Bitte alle Felder ausfüllen.")
            return

        try:
            cur.execute("SELECT benutzername FROM benutzer WHERE benutzername = ?", (email,))
            benutzername = cur.fetchone()
            cur.execute("SELECT benutzer.passwort_hash FROM benutzer WHERE benutzer.benutzername = ?",(benutzername[0],))
            row = cur.fetchone()
            passworthash = row[0]
            if bcrypt.checkpw(pw.encode(), passworthash.encode()):
                print ("Passwort stimmt überein!")
                passwort = True

            else:
                messagebox.showerror("Fehler", f"Passwort stimmt nicht überein!")
                print ("Passwort stimmt nicht überein!")


            if benutzername:
                print("Benutzername stimmt überein!")

            else:
                messagebox.showerror("Fehler", "Benutzername nicht gefunden.")

            if passwort and benutzername:
                messagebox.showinfo("Hinweis", f"Anmeldung für {email} erfolgreich.")

        except Exception as e:
            messagebox.showerror("Fehler", f"Anmeldung fehlgeschlagen: {e}")


