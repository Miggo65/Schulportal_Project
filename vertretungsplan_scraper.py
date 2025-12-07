#!/usr/bin/env python3
"""
Hauptskript zum Herunterladen und Speichern des Vertretungsplans
Integriert mit Stundenplan-Checker für personalisierte Benachrichtigungen
"""

from playwright.sync_api import sync_playwright
from datetime import datetime
import os

# Importieren meiner Schulportal_Library
from schulportal_lib import login, get_vertretungsplan
from stundenplan_checker import StundenplanChecker


def save_vertretungsplan_txt(data: dict, Vertretungsplan_saves: str = 'Vertretungsplan_saves') -> str:
    """
    Daten aus Library in Datei schreiben
    
    Args:
        data: Vertretungsplan-Daten
        Vertretungsplan_saves: Ordner für Speicherung
        
    Returns:
        Pfad zur gespeicherten Datei
    """
    # Erstelle output-Ordner falls nicht vorhanden
    os.makedirs(Vertretungsplan_saves, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    txt_file = f"{Vertretungsplan_saves}/vertretungsplan_{timestamp}.txt"
    
    with open(txt_file, 'w', encoding='utf-8') as f:
        # Zeit des Abrufs
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


def main():
    """Hauptfunktion"""
    print("\n" + "=" * 70)
    print("SCHULPORTAL VERTRETUNGSPLAN CHECKER")
    print("=" * 70)
    
    # Userdaten einlesen
    print("\nBitte Zugangsdaten eingeben:\n")
    
    USERNAME = input("Benutzername: ").strip()
    PASSWORD = input("Passwort: ").strip()
    INSTITUTION_ID = input("Institutions-ID (Standard: 6081): ").strip() or "6081"
    
    print()
    
    if not USERNAME or not PASSWORD:
        print("❌ Benutzername und Passwort können nicht leer sein!")
        return
    
    # Ruft Browser start function aus library ab
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome", 
            headless=True      
        )
        page = browser.new_page()
        
        try:
            # Login durchführen
            if not login(page, USERNAME, PASSWORD, INSTITUTION_ID):
                print("\n❌ Abbruch wegen Login-Fehler")
                return
            
            # Vertretungsplan get funktion aus Library abrufen
            Vertretungsplan_Inhalt = get_vertretungsplan(page)
            
            if not Vertretungsplan_Inhalt:
                print("\n❌ Abbruch - Fehler beim Abrufen vom Vertretungsplan")
                return
            
            # Vertretungsplan speichern Funktion aufrufen
            txt_file = save_vertretungsplan_txt(Vertretungsplan_Inhalt)
            print(f"✅ TXT-Datei gespeichert: {txt_file}")
            
            # Stundenplan-Abgleich durchführen
            print("\n" + "=" * 70)
            print("STARTE STUNDENPLAN-ABGLEICH")
            print("=" * 70)
            
            checker = StundenplanChecker()
            relevante_ausfaelle = checker.check_vertretungsplan(Vertretungsplan_Inhalt)
            
            # Zusätzliche Ausgabe für neue Ausfälle
            neue_ausfaelle = [a for a in relevante_ausfaelle if a['neu']]
            
            if neue_ausfaelle:
                print("\n" + "🚨" * 35)
                print("WICHTIG: NEUE AUSFÄLLE IN DEINEM STUNDENPLAN!")
                print("🚨" * 35)
                for ausfall in neue_ausfaelle:
                    print(f"📅 {ausfall['wochentag']}, {ausfall['datum']}")
                    print(f"   ⏰ Stunde {ausfall['stunde']}")
                    print(f"   👨‍🏫 Lehrer: {ausfall['lehrer']}")
                    print()
            else:
                print("\n✅ Keine neuen Ausfälle in deinem Stundenplan!")
            
        finally:
            browser.close()
    
    print("\n" + "=" * 70)
    print("PROGRAMM BEENDET")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
