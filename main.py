#imports

import tkinter as tk
import datenbankverbindung


root = tk.Tk()
root.geometry("500x300")
root.title("Als Benutzer anmelden: ")

datenbank = datenbankverbindung.Datenbank(root)
datenbank.datenbankverbindung()
#conn = datenbank.try_connect()
#cur = conn.cursor()


root.mainloop()

