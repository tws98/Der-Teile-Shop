import tkinter as tk
from tkinter import ttk, messagebox
import funktionen

import mariadb
import sys


class Datenbank ():
    def  __init__(self, parent):
        self.connected = False
        self.parent = parent
        self.frame = ttk.Frame(self.parent)
        self.conn = None
        self.entry_benutzer = None
        self.entry_passwort = None
        self.benutzername = ""
        self.passwort = ""


    def datenbankverbindung (self):
        frame = self.frame
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        ttk.Label(frame, text="Datenbankanmeldung", font=("Arial", 12, "bold")).pack(pady=10)

        ttk.Label(frame, text="Benutzer:").pack()
        self.entry_benutzer = ttk.Entry(frame)
        self.entry_benutzer.pack(pady=5)

        ttk.Label(frame, text="Passwort:").pack()
        self.entry_passwort = ttk.Entry(frame, show="*")
        self.entry_passwort.pack(pady=5)

        ttk.Button(frame, text="Registrieren", command=self.datenbank_registrierung).pack(pady=10)


    def datenbank_registrierung(self):
    # Nur wenn self.benutzername und self.passwort leer sind, aus Entry-Feldern lesen
        if not self.benutzername or not self.passwort:
            try:
                benutzer = self.entry_benutzer.get()
                passwort = self.entry_passwort.get()
            except Exception as e:
                messagebox.showerror("Fehler", f"Eintrag nicht verfügbar: {e}")
                return

            if not benutzer or not passwort:
                messagebox.showwarning("Fehler", "Bitte alle Felder ausfüllen.")
                return

        # Einmalig speichern
            self.benutzername = benutzer
            self.passwort = passwort

    # Verbindung aufbauen (egal ob neu oder zurückgekehrt)
        self.try_connect(self.benutzername, self.passwort)

        if self.connected:
            self.frame.destroy()
            print("Erfolgreich eingeloggt!")
            


        email = funktionen.Eingabe(self.parent)
        cur = self.conn.cursor()
        email.registrierung_ui(self.parent, cur, self.conn)
        email.anmeldung_ui(self.parent, cur, self.conn)

        return self.benutzername, self.passwort

    
    def try_connect(self, benutzer, passwort):
        # try:
        #     self.conn = mariadb.connect(
        #         host="10.80.0.206",
        #         port = 3306,
        #         user=benutzer,
        #         password=passwort,
        #         database="team04")
        #     self.connected = True

        try:
            self.conn = mariadb.connect(
                user = benutzer,
                password = passwort,
                host = "localhost",
                port = 3306,
                database = "projekt-legoshop")
            self.connected = True
            

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB PLatform: {e}")
            sys.exit(1)

