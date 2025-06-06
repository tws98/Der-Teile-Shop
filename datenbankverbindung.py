import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import funktionen
import mariadb
import sys
import os
from PIL import Image, ImageTk

# CustomTkinter Style Setup
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# Datenbank Klasse für die Verbindung
class Datenbank():
    def __init__(self, parent):
        self.connected = False
        self.parent = parent
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)

        # Linker Frame für das Formular
        self.frame = ctk.CTkFrame(self.main_frame)
        self.frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        # Rechter Frame für das Bild
        self.right_frame = ctk.CTkFrame(self.main_frame, width=200)
        self.right_frame.pack(side="right", padx=10, pady=10)

        self.conn = None
        self.entry_benutzer = None
        self.entry_passwort = None
        self.benutzername = ""
        self.passwort = ""
            
    # Logo aufrufen

    
    def zeige_logo(self):
        try:
            img_path = get_resource_path("Logo.png")
            if not os.path.isfile(img_path):
                raise FileNotFoundError("Logo-Datei nicht gefunden.")

            # Zielgröße des Bildes (muss zur Framegröße passen)
            target_width = 200
            target_height = 190

            # Bild laden und skalieren
            original_image = Image.open(img_path)
            resized_image = original_image.resize((target_width, target_height), Image.LANCZOS)
            logo_img = ImageTk.PhotoImage(resized_image)

            image_label = ctk.CTkLabel(self.right_frame, image=logo_img, text="")
            image_label.image = logo_img
            image_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden des Logos:\n{e}")


    # Funktion für die Verbindung zur Datenbank
    def datenbankverbindung(self):
        frame = self.frame
        self.zeige_logo()
        
        ctk.CTkLabel(frame, text="Datenbankanmeldung", font=("Arial", 12, "bold")).pack(pady=10)

        ctk.CTkLabel(frame, text="Benutzer:").pack()
        self.entry_benutzer = ctk.CTkEntry(frame)
        self.entry_benutzer.pack(pady=5)

        ctk.CTkLabel(frame, text="Passwort:").pack()
        self.entry_passwort = ctk.CTkEntry(frame, show="*")
        self.entry_passwort.pack(pady=5)

        self.use_local = ctk.BooleanVar(value=False)  # Standardmäßig zentral (Server) aktiv
        self.switch_local = ctk.CTkSwitch(
            frame,
            text="Lokale Verbindung aktivieren",
            variable=self.use_local,
            onvalue=True,
            offvalue=False)
        self.switch_local.pack(pady=5)

        ctk.CTkButton(frame, text="Registrieren", command=self.datenbank_registrierung).pack(pady=10)


    def datenbank_registrierung(self):
        # Nur wenn self.benutzername und self.passwort leer sind, aus Entry-Feldern lesen
        if not self.benutzername or not self.passwort:
            try:
                benutzer = self.entry_benutzer.get()
                passwort = self.entry_passwort.get()
            except Exception as e:
                messagebox.showerror("Fehler", f"Eintrag nicht verfügbar: {e}")
                return
        # Robuste Eingabe
            if not benutzer or not passwort:
                messagebox.showwarning("Fehler", "Bitte alle Felder ausfüllen.")
                return
            
        # Einmalig speichern
            self.benutzername = benutzer
            self.passwort = passwort

    # Verbindung aufbauen
        self.try_connect(self.benutzername, self.passwort)

    # Sobald Verbindung aufgebaut wurde, Übergabe an die funktionen Datei für den Aufbau der Benutzerregistrierung
        if self.connected:
            self.main_frame.destroy()

            email = funktionen.Eingabe(self.parent)
            cur = self.conn.cursor()
            email.registrierung_ui(self.parent, cur, self.conn)
            email.anmeldung_ui(self.parent, cur, self.conn)

        # Zum Speichern der Daten für die nachträgliche Sicherung
        return self.benutzername, self.passwort


        # Für den Logout Button im Nachhinein
    def zeige_benutzer_login(self):
        funktionen.Eingabe.clear_window(self, self.parent)
        if not self.connected:
            messagebox.showerror("Fehler", "Keine Datenbankverbindung!")
            return

        email_gui = funktionen.Eingabe(self.parent)
        cur = self.conn.cursor()
        email_gui.registrierung_ui(self.parent, cur, self.conn)
        email_gui.anmeldung_ui(self.parent, cur, self.conn)

        # Funktion um zu Entscheiden welche Datenbank verwendet werden soll
    def try_connect(self, benutzer, passwort):
        use_local = self.use_local.get() if hasattr(self, "use_local") else True

        try:
            if use_local:
                self.conn = mariadb.connect(
                    user=benutzer,
                    password=passwort,
                    host="localhost",
                    port=3306,
                    database="projekt-legoshop"
                )
            else:
                self.conn = mariadb.connect(
                    user=benutzer,
                    password=passwort,
                    host="10.80.0.206",
                    port=3306,
                    database="team04"
                )
            self.connected = True

        except mariadb.Error as e:
            print(f"Fehler bei Verbindung: {e}")
            sys.exit(1)

def get_resource_path(relativer_pfad):
        """Funktioniert sowohl im Entwicklermodus als auch in PyInstaller-Exe"""
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relativer_pfad)
        return os.path.join(os.path.abspath("."), relativer_pfad)
