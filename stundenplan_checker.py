#!/usr/bin/env python3
"""
Stundenplan-Checker
Gleicht den persönlichen Stundenplan mit dem Vertretungsplan ab
und meldet Ausfälle in der Konsole
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Set, Tuple


class StundenplanChecker:
    """Klasse zum Abgleichen von Stundenplan und Vertretungsplan"""
    
    WOCHENTAGE_DE = {
        0: "Montag",
        1: "Dienstag", 
        2: "Mittwoch",
        3: "Donnerstag",
        4: "Freitag",
        5: "Samstag",
        6: "Sonntag"
    }
    
    def __init__(self, stundenplan_datei: str = "Stundenplan.txt", 
                 tracking_datei: str = "known_ausfaelle.json"):
        """
        Initialisiert den Checker
        
        Args:
            stundenplan_datei: Pfad zur Stundenplan-Datei
            tracking_datei: Pfad zur JSON-Datei für bereits gemeldete Ausfälle
        """
        self.stundenplan_datei = stundenplan_datei
        self.tracking_datei = tracking_datei
        self.stundenplan = self._parse_stundenplan()
        self.known_ausfaelle = self._load_known_ausfaelle()
    
    def _parse_stundenplan(self) -> Dict[str, Dict[int, str]]:
        """
        Parst die Stundenplan.txt Datei
        
        Returns:
            Dictionary: {wochentag: {stunde: lehrerkuerzel}}
        """
        stundenplan = {}
        
        if not os.path.exists(self.stundenplan_datei):
            print(f"⚠️  Warnung: {self.stundenplan_datei} nicht gefunden!")
            return stundenplan
        
        with open(self.stundenplan_datei, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_day = None
        
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
            
            # Prüfe ob es ein Wochentag ist
            if line in self.WOCHENTAGE_DE.values():
                current_day = line
                stundenplan[current_day] = {}
            elif current_day and '=' in line:
                # Parse Stundenzeile: "Stunde 1 = Shm"
                parts = line.split('=')
                if len(parts) == 2:
                    stunden_text = parts[0].strip()
                    lehrer = parts[1].strip()
                    
                    # Extrahiere Stundennummer
                    if 'Stunde' in stunden_text:
                        try:
                            stunde_num = int(stunden_text.split()[1])
                            if lehrer != "None":
                                stundenplan[current_day][stunde_num] = lehrer
                        except (ValueError, IndexError):
                            pass
        
        return stundenplan
    
    def _load_known_ausfaelle(self) -> Set[str]:
        """
        Lädt bereits gemeldete Ausfälle aus JSON-Datei
        
        Returns:
            Set mit IDs bereits gemeldeter Ausfälle
        """
        if not os.path.exists(self.tracking_datei):
            return set()
        
        try:
            with open(self.tracking_datei, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return set(data.get('ausfaelle', []))
        except Exception as e:
            print(f"⚠️  Warnung: Fehler beim Laden von {self.tracking_datei}: {e}")
            return set()
    
    def _save_known_ausfaelle(self):
        """Speichert bekannte Ausfälle in JSON-Datei"""
        try:
            data = {
                'ausfaelle': list(self.known_ausfaelle),
                'letzte_aktualisierung': datetime.now().isoformat()
            }
            with open(self.tracking_datei, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Warnung: Fehler beim Speichern von {self.tracking_datei}: {e}")
    
    def _create_ausfall_id(self, datum: str, stunde: str, lehrer: str) -> str:
        """
        Erstellt eine eindeutige ID für einen Ausfall
        
        Args:
            datum: Datum des Ausfalls
            stunde: Stundennummer
            lehrer: Lehrerkürzel
            
        Returns:
            Eindeutige ID als String
        """
        return f"{datum}_{stunde}_{lehrer}"
    
    def _parse_datum(self, datum_str: str) -> Tuple[str, str]:
        """
        Parst Datum aus Vertretungsplan
        
        Args:
            datum_str: Datum-String (z.B. "01.12.2025heute49.")
            
        Returns:
            Tuple: (sauberes Datum "01.12.2025", Wochentag)
        """
        # Extrahiere nur das Datum im Format DD.MM.YYYY
        datum_clean = ""
        for part in datum_str.split():
            if '.' in part and len(part) >= 8:
                # Finde das Datum-Pattern
                import re
                match = re.search(r'(\d{2}\.\d{2}\.\d{4})', part)
                if match:
                    datum_clean = match.group(1)
                    break
        
        if not datum_clean:
            datum_clean = datum_str
        
        # Bestimme Wochentag aus Datum
        try:
            date_obj = datetime.strptime(datum_clean, '%d.%m.%Y')
            wochentag = self.WOCHENTAGE_DE[date_obj.weekday()]
        except:
            wochentag = "Unbekannt"
        
        return datum_clean, wochentag
    
    def check_vertretungsplan(self, vertretungsplan_data: dict) -> List[dict]:
        """
        Gleicht Vertretungsplan mit persönlichem Stundenplan ab
        
        Args:
            vertretungsplan_data: Dictionary mit Vertretungsplan-Daten
            
        Returns:
            Liste mit relevanten Ausfällen
        """
        relevante_ausfaelle = []
        neue_ausfaelle_count = 0
        bereits_bekannt_count = 0
        
        print("\n" + "=" * 70)
        print("STUNDENPLAN-ABGLEICH")
        print("=" * 70)
        
        # Iteriere durch alle Tage im Vertretungsplan
        for tag in vertretungsplan_data.get('tage', []):
            datum_raw = tag.get('datum', 'Unbekannt')
            datum, wochentag = self._parse_datum(datum_raw)
            
            print(f"\n📅 Prüfe {wochentag}, {datum}")
            
            # Hole den Stundenplan für diesen Wochentag
            mein_stundenplan = self.stundenplan.get(wochentag, {})
            
            if not mein_stundenplan:
                print(f"   ℹ️  Kein Unterricht laut Stundenplan")
                continue
            
            # Prüfe Vertretungen für diesen Tag
            vertretungen = tag.get('vertretungen')
            if not vertretungen or vertretungen.get('row_count', 0) == 0:
                print(f"   ✅ Keine Vertretungen/Ausfälle")
                continue
            
            headers = vertretungen.get('headers', [])
            rows = vertretungen.get('rows', [])
            
            # Finde Index der relevanten Spalten
            try:
                stunde_idx = headers.index('Stunde')
                lehrer_idx = headers.index('Lehrer')
                art_idx = headers.index('Art')
            except ValueError as e:
                print(f"   ⚠️  Fehler beim Parsen der Tabelle: {e}")
                continue
            
            # Prüfe jede Vertretungszeile
            for row in rows:
                if len(row) <= max(stunde_idx, lehrer_idx, art_idx):
                    continue
                
                stunde_str = row[stunde_idx].strip()
                lehrer = row[lehrer_idx].strip()
                art = row[art_idx].strip()
                
                # Prüfe ob es ein Entfall ist
                if 'Entfall' not in art:
                    continue
                
                # Parse Stundennummer (kann "3" oder "9 - 10" sein)
                stunden = []
                if '-' in stunde_str:
                    parts = stunde_str.split('-')
                    try:
                        start = int(parts[0].strip())
                        end = int(parts[1].strip())
                        stunden = list(range(start, end + 1))
                    except ValueError:
                        continue
                else:
                    try:
                        stunden = [int(stunde_str)]
                    except ValueError:
                        continue
                
                # Prüfe ob eine dieser Stunden in meinem Stundenplan ist
                for stunde in stunden:
                    if stunde in mein_stundenplan:
                        mein_lehrer = mein_stundenplan[stunde]
                        
                        # Prüfe ob es der gleiche Lehrer ist
                        if mein_lehrer == lehrer:
                            # Erstelle Ausfall-ID
                            ausfall_id = self._create_ausfall_id(datum, str(stunde), lehrer)
                            
                            # Prüfe ob bereits bekannt
                            is_new = ausfall_id not in self.known_ausfaelle
                            
                            ausfall_info = {
                                'datum': datum,
                                'wochentag': wochentag,
                                'stunde': stunde,
                                'lehrer': lehrer,
                                'neu': is_new,
                                'ausfall_id': ausfall_id
                            }
                            
                            relevante_ausfaelle.append(ausfall_info)
                            
                            if is_new:
                                print(f"   🚨 NEUER AUSFALL: Stunde {stunde} ({lehrer}) fällt aus!")
                                self.known_ausfaelle.add(ausfall_id)
                                neue_ausfaelle_count += 1
                            else:
                                print(f"   🔄 [DEBUG] Bereits bekannt: Stunde {stunde} ({lehrer}) fällt aus")
                                bereits_bekannt_count += 1
        
        # Speichere aktualisierte Liste der bekannten Ausfälle
        if neue_ausfaelle_count > 0:
            self._save_known_ausfaelle()
        
        # Zusammenfassung
        print("\n" + "=" * 70)
        print("ZUSAMMENFASSUNG")
        print("=" * 70)
        print(f"🆕 Neue Ausfälle: {neue_ausfaelle_count}")
        print(f"🔄 Bereits bekannte Ausfälle: {bereits_bekannt_count}")
        print(f"📊 Gesamt: {len(relevante_ausfaelle)}")
        print("=" * 70 + "\n")
        
        return relevante_ausfaelle


def main():
    """Test-Funktion"""
    print("\n" + "=" * 70)
    print("STUNDENPLAN-CHECKER - TEST")
    print("=" * 70)
    
    # Erstelle Checker
    checker = StundenplanChecker()
    
    # Zeige geladenen Stundenplan
    print("\n📚 Geladener Stundenplan:")
    for tag, stunden in checker.stundenplan.items():
        print(f"\n{tag}:")
        for stunde, lehrer in sorted(stunden.items()):
            print(f"  Stunde {stunde}: {lehrer}")
    
    print("\n✅ Checker initialisiert!")
    print("💡 Verwende check_vertretungsplan(data) mit Vertretungsplan-Daten")


if __name__ == "__main__":
    main()
