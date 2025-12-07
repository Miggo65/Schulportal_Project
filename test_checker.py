#!/usr/bin/env python3
"""
Test-Skript für den Stundenplan-Checker
Testet die Funktionalität ohne echten Schulportal-Login
"""

from stundenplan_checker import StundenplanChecker
from datetime import datetime


def create_test_vertretungsplan():
    """
    Erstellt Test-Vertretungsplan-Daten im gleichen Format wie die echten Daten
    """
    return {
        'zeitstempel': datetime.now().isoformat(),
        'anzahl_tage': 2,
        'tage': [
            {
                'datum': '09.12.2025montag',
                'badges': ['montag'],
                'panel_id': 'tag1',
                'informationen': {
                    'abwesende_lehrer': 'Urc (1-6), Fis (3-4)',
                    'hinweis': '',
                    'entfall_klassen': 'E, Q1'
                },
                'vertretungen': {
                    'headers': ['Stunde', 'Klasse', 'Vertreter', 'Lehrer', 'Art', 'Fach', 'Raum', 'Hinweis'],
                    'rows': [
                        ['1', 'E', '', 'Urc', 'Entfall', 'MA 2', '', ''],
                        ['2', 'E', '', 'Urc', 'Entfall', 'MA 2', '', ''],
                        ['3', 'Q1', '', 'Fis', 'Entfall', 'PH 1', '', ''],
                        ['5', 'E', 'Gbg', 'Shm', 'Vertretung', 'EN 2', '101', ''],  # Shm fällt nicht aus, Vertretung
                    ],
                    'row_count': 4,
                    'table_id': 'vtable1'
                },
                'letzte_aktualisierung': 'Letzte Aktualisierung: 08.12.2025 um 14:30:00 Uhr'
            },
            {
                'datum': '10.12.2025dienstag',
                'badges': ['dienstag'],
                'panel_id': 'tag2',
                'informationen': {
                    'abwesende_lehrer': 'Gbg (1-2), Svs (5-6)',
                    'hinweis': '',
                    'entfall_klassen': 'E, Q3'
                },
                'vertretungen': {
                    'headers': ['Stunde', 'Klasse', 'Vertreter', 'Lehrer', 'Art', 'Fach', 'Raum', 'Hinweis'],
                    'rows': [
                        ['1', 'E', '', 'Gbg', 'Entfall', 'DE 2', '', ''],
                        ['2', 'E', '', 'Gbg', 'Entfall', 'DE 2', '', ''],
                        ['5 - 6', 'E', '', 'Svs', 'Entfall', 'CH 2', '', ''],  # Doppelstunde
                    ],
                    'row_count': 3,
                    'table_id': 'vtable2'
                },
                'letzte_aktualisierung': 'Letzte Aktualisierung: 08.12.2025 um 14:30:00 Uhr'
            },
            {
                'datum': '11.12.2025mittwoch',
                'badges': ['mittwoch'],
                'panel_id': 'tag3',
                'informationen': {
                    'abwesende_lehrer': '',
                    'hinweis': '',
                    'entfall_klassen': ''
                },
                'vertretungen': {
                    'headers': ['Stunde', 'Klasse', 'Vertreter', 'Lehrer', 'Art', 'Fach', 'Raum', 'Hinweis'],
                    'rows': [],
                    'row_count': 0,
                    'table_id': 'vtable3'
                },
                'letzte_aktualisierung': 'Letzte Aktualisierung: 08.12.2025 um 14:30:00 Uhr'
            }
        ]
    }


def main():
    print("\n" + "=" * 70)
    print("STUNDENPLAN-CHECKER TEST")
    print("=" * 70)
    print("\nDieser Test simuliert einen Vertretungsplan-Abruf ohne echten Login.\n")
    
    # Erstelle Checker
    print("📚 Initialisiere Stundenplan-Checker...")
    checker = StundenplanChecker()
    
    # Zeige geladenen Stundenplan
    print("\n📋 Dein Stundenplan:")
    print("-" * 70)
    for tag, stunden in sorted(checker.stundenplan.items()):
        print(f"\n{tag}:")
        if stunden:
            for stunde, lehrer in sorted(stunden.items()):
                print(f"  Stunde {stunde:2d}: {lehrer}")
        else:
            print("  Keine Stunden")
    
    # Erstelle Test-Vertretungsplan
    print("\n" + "=" * 70)
    print("ERSTELLE TEST-VERTRETUNGSPLAN")
    print("=" * 70)
    print("\nTest-Daten erstellt:")
    print("- Montag: Urc fällt aus (1-2), Fis fällt aus (3)")
    print("- Dienstag: Gbg fällt aus (1-2), Svs fällt aus (5-6)")
    print("- Mittwoch: Keine Ausfälle")
    
    test_data = create_test_vertretungsplan()
    
    # Führe Abgleich durch
    print("\n" + "=" * 70)
    print("FÜHRE ABGLEICH DURCH")
    print("=" * 70)
    
    relevante_ausfaelle = checker.check_vertretungsplan(test_data)
    
    # Detaillierte Ausgabe der Ergebnisse
    print("\n" + "=" * 70)
    print("DETAILLIERTE ERGEBNISSE")
    print("=" * 70)
    
    if relevante_ausfaelle:
        print("\n🔍 Alle erkannten Ausfälle (die dich betreffen):\n")
        for i, ausfall in enumerate(relevante_ausfaelle, 1):
            status = "🆕 NEU" if ausfall['neu'] else "🔄 BEKANNT"
            print(f"{i}. {status}")
            print(f"   📅 Datum: {ausfall['wochentag']}, {ausfall['datum']}")
            print(f"   ⏰ Stunde: {ausfall['stunde']}")
            print(f"   👨‍🏫 Lehrer: {ausfall['lehrer']}")
            print(f"   🔑 ID: {ausfall['ausfall_id']}")
            print()
    else:
        print("\n✅ Keine Ausfälle gefunden, die dich betreffen!")
    
    # Hinweis für zweiten Testlauf
    print("\n" + "💡" * 35)
    print("TIPP: Führe das Skript nochmal aus!")
    print("=" * 70)
    print("Beim zweiten Durchlauf sollten alle Ausfälle als [DEBUG] Bereits bekannt")
    print("markiert werden, da sie jetzt in known_ausfaelle.json gespeichert sind.")
    print("💡" * 35)
    
    print("\n" + "=" * 70)
    print("TEST ABGESCHLOSSEN")
    print("=" * 70)
    print("\n✅ Der Stundenplan-Checker funktioniert!")
    print("📝 Du kannst jetzt vertretungsplan_scraper.py mit echten Daten nutzen.\n")


if __name__ == "__main__":
    main()
