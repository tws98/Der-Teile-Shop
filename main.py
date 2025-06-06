import customtkinter as ctk
import datenbankverbindung

# CustomTkinter konfigurieren
ctk.set_appearance_mode("system")  # Optional: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # Optional: andere Themes verfügbar

# Hauptfenster erstellen
root = ctk.CTk()
root.geometry("550x400")
root.title("Als Benutzer anmelden: ")

# Datenbankobjekt erstellen und Verbindung aufbauen
datenbank = datenbankverbindung.Datenbank(root)
datenbank.datenbankverbindung()

# Hauptloop starten
root.mainloop()

