#imports

import tkinter as tk
import datenbankverbindung


root = tk.Tk()
root.geometry("500x300")
root.title("Als Benutzer anmelden: ")

datenbank = datenbankverbindung.Datenbank(root)
datenbank.datenbankverbindung()


root.mainloop()

# To-Dos:
# Änderungen der Kundendaten speichern und in Datenbank integrieren
# (darauf achten, dass die Fremdschlüssel richtig verwendet werden)
# logout-Funktion richtigstellen
# Admin menü - Kundenmenü gestalten - in einer Art Textbox ausgeben