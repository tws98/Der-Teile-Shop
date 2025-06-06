import customtkinter as ctk
import tkinter as tk
import funktionen

#Gesamtfunktion damit der Abruf in einem anderen Modul gewährleistet wird
def starte_produkt_gui(parent, cur, conn):
    # Meldebestand 
    meldebestand = 40

    # GUI-Konfiguration
    ctk.set_appearance_mode("system") # Optional: "Light", "Dark", "System"
    ctk.set_default_color_theme("blue") # Optional: andere Themes verfügbar

    #Grundrahmen
    root = ctk.CTk()
    root.title("Produktübersicht & Lagerstatus")
    root.geometry("550x400")

    haupt_rahmen = ctk.CTkFrame(root)
    haupt_rahmen.pack(fill="both", expand=True, padx=20, pady=20)

    linker_rahmen = ctk.CTkFrame(haupt_rahmen, width=300)
    linker_rahmen.pack(side="left", fill="y", padx=10)

    rechter_rahmen = ctk.CTkFrame(haupt_rahmen)
    rechter_rahmen.pack(side="right", fill="both", expand=True, padx=10)

    #Initalisierung eines Dictionarys für die Prduktauswahl
    produkt_zuordnung = {}

    def lade_produkte():
        cur.execute("""
            SELECT 
                produkte.produktid,
                stein.Stein,
                farbe.farbe
            FROM 
                produkte
            JOIN 
                stein ON produkte.SteinID = stein.SteinID
            JOIN 
                farbe ON produkte.FarbID = farbe.farbid
            GROUP BY produkte.produktid;
        """)
        zeilen = cur.fetchall()
        produkt_zuordnung.clear()
        produkt_auswahl.configure(values=[])

        for zeile in zeilen:
            anzeige = f"{zeile[0]} – {zeile[1]} ({zeile[2]})"
            produkt_zuordnung[anzeige] = zeile[0]

        produkt_auswahl.configure(values=list(produkt_zuordnung.keys()))

    #Funktion damit sich die Details zu einem Produkt anzeigen lassen
    def zeige_produktdetails():
        auswahl = produkt_auswahl.get()
        if auswahl not in produkt_zuordnung:
            details_feld.delete("1.0", tk.END)
            details_feld.insert(tk.END, "Bitte ein Produkt auswählen.")
            details_feld.see(tk.END)
            return

        produktid = produkt_zuordnung[auswahl]
        cur.execute("""
            SELECT 
                produkte.produktid,
                stein.Stein,
                farbe.farbe,
                produkte.Lagerbestand,
                produkte.preis
            FROM 
                produkte
            JOIN 
                stein ON produkte.SteinID = stein.SteinID
            JOIN 
                farbe ON produkte.FarbID = farbe.farbid
            WHERE produkte.produktid = ?
        """, (produktid,))

        zeile = cur.fetchone()

        details_feld.delete("1.0", tk.END)

        if zeile:
            bestand = zeile[3]
            text = (
                f"Produkt ID: {zeile[0]}\n"
                f"Typ: {zeile[1]}\n"
                f"Farbe: {zeile[2]}\n"
                f"Lagerbestand: {bestand}\n"
                f"Meldebestand: {meldebestand}\n"
                f"Preis: {zeile[4]}€"
            )
            details_feld.insert(tk.END, text)

            if bestand < meldebestand:
                warnung = "\n\n⚠️ Bestand unter Meldebestand!"
                details_feld.insert(tk.END, warnung)
                details_feld.tag_add("warnung", f"end-{len(warnung)+1}c", "end")
                details_feld.tag_config("warnung", foreground="red", font=("Arial", 16, "bold"))
            details_feld.see(tk.END)
        else:
            details_feld.insert(tk.END, "Produkt nicht gefunden.")
            details_feld.see(tk.END)

    #Widgets der GUI 
    produkt_auswahl = ctk.CTkComboBox(linker_rahmen, width=280, state="readonly")
    produkt_auswahl.pack(pady=10)

    anzeigen_button = ctk.CTkButton(linker_rahmen, text="Details anzeigen", command=zeige_produktdetails)
    anzeigen_button.pack(pady=5)

    details_feld = tk.Text(rechter_rahmen, font=("Arial", 16), wrap="word", bg="white", fg="black")
    scroll_leiste = tk.Scrollbar(rechter_rahmen, command=details_feld.yview)
    details_feld.configure(yscrollcommand=scroll_leiste.set)

    scroll_leiste.pack(side="right", fill="y")
    details_feld.pack(fill="both", expand=True, padx=10, pady=10)

    def zurueck_zum_hauptmenue():
        root.destroy()
        eingabe = funktionen.Eingabe(parent)
        eingabe.hauptmenu_admin(parent, cur, conn)

    zurueck_button = ctk.CTkButton(linker_rahmen, text="Zurück", command=zurueck_zum_hauptmenue)
    zurueck_button.pack(pady=(0, 5))

    lade_produkte()
    if produkt_zuordnung:
        erster_schluessel = list(produkt_zuordnung.keys())[0]
        produkt_auswahl.set(erster_schluessel)
        zeige_produktdetails()

    root.mainloop()
