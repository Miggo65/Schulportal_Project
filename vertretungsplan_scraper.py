

#Hauptskript zum Herunterladen und Speichern des Vertretungsplans


from playwright.sync_api import sync_playwright
from datetime import datetime
import os

# Importieren meiner Schulportal_Libary
from schulportal_lib import login, get_vertretungsplan


#Daten aus Libary in Datei schreiben
def save_vertretungsplan_txt(data: dict, Vertretungsplan_saves: str = 'output') -> str:
    
    # Erstelle output-Ordner falls nicht vorhanden
    os.makedirs(Vertretungsplan_saves, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    txt_file = f"{Vertretungsplan_saves}/vertretungsplan_{timestamp}.txt"
    
    with open(txt_file, 'w', encoding='utf-8') as f:
        #Zeit des Abrufs
        f.write(f"Abgerufen: {data['zeitstempel']}\n")

        
        for day in data['tage']:
            f.write("=" * 70 + "\n")
            f.write(f"DATUM: {day['datum']}\n")
            
            # Vertretungen
            if day['vertretungen'] and day['vertretungen']['row_count'] > 0:
                f.write("VERTRETUNGEN\n")
                f.write("-" * 70 + "\n")
                
                # Header
                headers = day['vertretungen']['headers']
                f.write(" | ".join(headers) + "\n")
                f.write("-" * 70 + "\n")
                
                # Zeilen
                for row in day['vertretungen']['rows']:
                    f.write(" | ".join(row) + "\n")
                


            else:
                f.write("VERTRETUNGEN\n")
                f.write("-" * 70 + "\n")
                f.write("Keine Vertretungen\n")
            
            f.write("\n\n")
    
    return txt_file





#Hauptfunktion
def main():

    print("\n" + "=" * 60)
    print("SCHULPORTAL VERTRETUNGSPLAN DOWNLOADER")
    print("=" * 60)

    
    #Userdaten einlesen
    print("Bitte Zugangsdaten eingeben:\n")
    
    USERNAME = input("Benutzername: ").strip()
    PASSWORD = input("Passwort: ").strip()
    INSTITUTION_ID = input("Institutions-ID (Standard: 6081): ").strip() or "6081"
    
    print()
    
    if not USERNAME or not PASSWORD:
        print("Benutzername und Passwort können nicht leer sein!")
        return
     

    #Ruft Browser start function aus libary ab.
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome", 
            headless=True      
        )
        page = browser.new_page()
        
        try:
            # Login durchführen
            if not login(page, USERNAME, PASSWORD, INSTITUTION_ID):
                print("\n Abbruch wegen Login-Fehler")
                return
            
            # Vertretungsplan_ get funktion aus Libary abrufen
            Vertretungsplan_Inhalt = get_vertretungsplan(page)
            
            if not Vertretungsplan_Inhalt:
                print("\n Abbruch - Fehler beim abrufen vom Vertretungsplan")
                return
            

            #Vertretugsplan speichern Funktion augrufen
            txt_file = save_vertretungsplan_txt(Vertretungsplan_Inhalt)
            print(f" TXT-Datei gespeichert: {txt_file}")

            
        finally:
            browser.close()


main()
