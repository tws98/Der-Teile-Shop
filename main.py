#imports

import tkinter as tk
import datenbankverbindung


root = tk.Tk()
root.geometry("500x300")
root.title("Datenbank Registrierung")

datenbank = datenbankverbindung.Datenbank(root)
datenbank.datenbankverbindung()


root.mainloop()
