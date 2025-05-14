#imports
 
import bcrypt
import mysql.connector
import mariadb
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Benutzer ():
    def __init__(self,id,benutzername,passwort_hash,rolle,kunden_id):
        self.id = id
        self.benutzername = benutzername
        self.passwort = passwort_hash
        self.rolle = rolle
        self.kunden_id = kunden_id


# Verbindung zur Datenbank aufbauen
try:
    conn = mariadb.connect(
        host="localhost",
        port = 3306,
        user="admin",
        password="admin",
        database="projekt-legoshop")
    
except mariadb.Error as e:
    print(f"Error connecting to MariaDB PLatform: {e}")
    sys.exit(1)
cur = conn.cursor()


# Fenster 2: Passwort setzen
def fenster_passwort():
    pw_window = tk.Tk()
    pw_window.geometry("400x200")
    pw_window.title("Passwort setzen")
    label_pw = ttk.Label(pw_window, text="Passwort: ")
    label_pw.pack(pady=10)
    pw_entry = ttk.Entry(pw_window)
    pw_entry.pack(pady=5)

    pw_window.mainloop()

# Funktion für Button 'Anmelden' - Prüfen ob Email vorhanden ist
def pruefe_email():
    emailneu = entry.get()
    # Eingegebene Email auf vorhandene Emails in Datenbank prüfen
    cur.execute("""SELECT kunden.Email FROM kunden WHERE kunden.Email = 'longglied@gmx.net';""")
    # Ergebnis der SQL-Abfrage in Variable emailalt speichern
    emailalt = cur.fetchone()
    print (emailneu)

    # Prüfung ob beide e-mails gleich sind:
    if emailalt and emailneu == emailalt[0]:
        print("E-Mails sind gleich")
        root.destroy()
        fenster_passwort()
        
    
    else:
        print("Email unterschiedlich")



# GUI Fenster 1: Email prüfen

root = tk.Tk()
root.geometry("400x200")
root.title("Als Benutzer anmelden: ")

label_user = ttk.Label(root, text="E-Mail Adresse: ")
entry = ttk.Entry(root)

label_user.pack(pady=10)
entry.pack(pady=5)
ttk.Button(root,text="Anmelden", command=pruefe_email).pack(pady=5)

root.mainloop()



# Fenster 3: Neue Kundendaten
def fenster_kundendaten():
    daten_window = tk.Tk()
    daten_window.title("Kundendaten eingeben")

    tk.Label(daten_window, text="Vorname:").pack()
    tk.Entry(daten_window).pack()
    tk.Label(daten_window, text="Nachname:").pack()
    tk.Entry(daten_window).pack()
    tk.Button(daten_window, text="Speichern").pack()

    daten_window.mainloop()
