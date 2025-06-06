import mariadb
import funktionen
import customtkinter as ctk


#Gesamtfunktion damit der Abruf in einem anderen Modul gewährleistet wird
def starte_auftrag_gui(parent, cur, conn):
    # GUI-Einstellungen
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    #Grundrahmen
    root = ctk.CTk()
    root.title("Auftragserfassung")
    root.geometry("300x600")


    haupt_rahmen = ctk.CTkFrame(root)
    haupt_rahmen.pack(fill="both", expand=True, padx=20, pady=20)


    haupt_rahmen.grid_columnconfigure(0, weight=3)  
    haupt_rahmen.grid_columnconfigure(1, weight=2)  
    haupt_rahmen.grid_rowconfigure(0, weight=1)


    linker_bereich = ctk.CTkFrame(haupt_rahmen)
    linker_bereich.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)




    # Dictionaries für Zuordnung
    farb_dict = {}
    stein_dict = {}

    #Funktion Kundensuche
    def suche_kunde(cur):
        kunden_id = eingabe_kundenid.get()
        try:
            cur.execute("SELECT vorname, name FROM kunden WHERE IDKunde = ?", (kunden_id,))
            row = cur.fetchone()
            if row:
                kundeninfo_label.configure(text=f"Kunde: {row[0]} {row[1]}")
            else:
                kundeninfo_label.configure(text="Kunde nicht gefunden")
        except mariadb.Error as e:
            kundeninfo_label.configure(text="Fehler bei Kundensuche")

    #Funktion Dropdown Menus

    def lade_dropdowns(cur):
        #Farb Auswahl
        cur.execute("SELECT farbid, farbe FROM farbe")
        farben = cur.fetchall()
        farb_dict.clear()
        farb_auswahl.configure(values=[f"{row[1]}" for row in farben])
        for row in farben:
            farb_dict[row[1]] = row[0]

        #Stein Auswahl
        cur.execute("SELECT steinid, stein FROM stein")
        steine = cur.fetchall()
        stein_dict.clear()
        stein_auswahl.configure(values=[f"{row[1]}" for row in steine])
        for row in steine:
            stein_dict[row[1]] = row[0]

    #Funktion Auftragserfassung

    def erfasse_auftrag():
        kunden_id = eingabe_kundenid.get()
        farbe = farb_auswahl.get()
        stein = stein_auswahl.get()
        menge = menge_entry.get()

        if not kunden_id.isdigit():
            auftragsinfo_label.configure(text="Ungültige Kunden-ID!", text_color="red")
            return
        if farbe == "":
            auftragsinfo_label.configure(text="Bitte Farbe auswählen!", text_color="red")
            return
        if stein == "":
            auftragsinfo_label.configure(text="Bitte Stein auswählen!", text_color="red")
            return
        if not menge.isdigit() or int(menge) <= 0:
            auftragsinfo_label.configure(text="Menge muss eine positive Zahl sein!", text_color="red")
            return

        farb_id = farb_dict.get(farbe)
        stein_id = stein_dict.get(stein)

        if farb_id is None or stein_id is None:
            auftragsinfo_label.configure(text="Farbe oder Stein ungültig!", text_color="red")
            return

        try:
            cur.execute(
                "SELECT produktid FROM produkte WHERE SteinID = ? AND FarbID = ?",
                (stein_id, farb_id,))
            row = cur.fetchone()
            if not row:
                auftragsinfo_label.configure(text="Produkt nicht gefunden!", text_color="red")
                return
            produktid = row[0]

            cur.execute(
                "INSERT INTO aufträge (IDKunde, produktid) VALUES (?, ?)",
                (int(kunden_id), produktid))
            conn.commit()

            cur.execute(
                "SELECT auftragsid FROM aufträge WHERE IDKunde = ? ORDER BY auftragsid DESC LIMIT 1",
                (kunden_id,))
            row = cur.fetchone()
            if row is None:
                auftragsinfo_label.configure(text="Fehler: Auftrag nicht gefunden!", text_color="red")
                return
            idauftrag = row[0]

            cur.execute("INSERT INTO auftragsposition (idprodukt, idauftrag, Menge) VALUES (?, ?, ?)",
                        (produktid, idauftrag, int(menge)))
            conn.commit()

            cur.execute("SELECT Lagerbestand FROM produkte WHERE produktid = ?", (produktid,))
            row = cur.fetchone()
            bestand = row[0]
            bestandneu = bestand - int(menge)
            cur.execute("UPDATE produkte SET Lagerbestand = ? WHERE produktid = ?", (bestandneu, produktid))
            conn.commit()

            auftragsinfo_label.configure(text="✅ Auftrag erfolgreich gespeichert!", text_color="green")
        except mariadb.Error as e:
            auftragsinfo_label.configure(text=f"Fehler beim Speichern: {e}", text_color="red")


    #Wigdets für die GUI 
    ctk.CTkLabel(linker_bereich, text="Kunden-ID eingeben:").pack(pady=(10, 0))
    eingabe_kundenid = ctk.CTkEntry(linker_bereich, width=200)
    eingabe_kundenid.pack(pady=5)

    suche_button = ctk.CTkButton(linker_bereich, text="Kunde suchen", command=lambda: suche_kunde(cur))
    suche_button.pack(pady=5)

    kundeninfo_label = ctk.CTkLabel(linker_bereich, text="Kunde: ", font=("Arial", 14))
    kundeninfo_label.pack(pady=5)

    ctk.CTkLabel(linker_bereich, text="Farbe auswählen:").pack(pady=(20, 0))
    farb_auswahl = ctk.CTkComboBox(linker_bereich, width=200, state="readonly")
    farb_auswahl.pack(pady=5)

    ctk.CTkLabel(linker_bereich, text="Stein auswählen:").pack(pady=(20, 0))
    stein_auswahl = ctk.CTkComboBox(linker_bereich, width=200, state="readonly")
    stein_auswahl.pack(pady=5)

    ctk.CTkLabel(linker_bereich, text="Menge:").pack(pady=(20, 0))
    menge_entry = ctk.CTkEntry(linker_bereich, width=100)
    menge_entry.pack(pady=5)

    speichern_button = ctk.CTkButton(linker_bereich, text="Auftrag speichern", command=erfasse_auftrag)
    speichern_button.pack(pady=10)

    auftragsinfo_label = ctk.CTkLabel(linker_bereich, text="", font=("Arial", 12))
    auftragsinfo_label.pack(pady=5)

    def zurueck_zum_hauptmenue():
        root.destroy()
        eingabe = funktionen.Eingabe(parent)
        eingabe.hauptmenu_admin(parent, cur, conn)

    zurueck_button = ctk.CTkButton(linker_bereich, text="Zurück", command=zurueck_zum_hauptmenue)
    zurueck_button.pack(pady=(0, 5))
            
    lade_dropdowns(cur)    
    root.mainloop()