# Schulportal Vertretungsplan Checker 🏫

Automatischer Vertretungsplan-Checker für das Schulportal Hessen mit personalisierten Benachrichtigungen basierend auf deinem Stundenplan.

## Features ✨

- ✅ Automatischer Login ins Schulportal Hessen
- ✅ Abruf des aktuellen Vertretungsplans
- ✅ Abgleich mit persönlichem Stundenplan
- ✅ Intelligente Erkennung relevanter Ausfälle
- ✅ Tracking bereits gemeldeter Ausfälle (verhindert Duplikate)
- ✅ Klare Konsolen-Ausgabe mit neuen vs. bekannten Ausfällen
- 🔜 Automatische Ausführung alle 5 Minuten
- 🔜 Discord-Benachrichtigungen bei neuen Ausfällen

## Projektstruktur 📁

```
Schulportal_Project/
├── schulportal_lib.py          # Library für Schulportal-Interaktion
├── stundenplan_checker.py      # Stundenplan-Abgleich-Logik
├── vertretungsplan_scraper.py  # Hauptskript
├── Stundenplan.txt             # Dein persönlicher Stundenplan
├── known_ausfaelle.json        # Tracking bereits gemeldeter Ausfälle (automatisch erstellt)
└── Vertretungsplan_saves/      # Gespeicherte Vertretungspläne
```

## Installation 🚀

### Voraussetzungen

- Python 3.8+
- Chrome/Chromium Browser

### Dependencies installieren

```bash
pip install playwright beautifulsoup4
playwright install chrome
```

## Konfiguration ⚙️

### Stundenplan.txt anpassen

Bearbeite die `Stundenplan.txt` Datei mit deinem persönlichen Stundenplan:

```
Montag
Stunde 1 = Shm
Stunde 2 = None
Stunde 3 = Fsc
...

Dienstag
Stunde 1 = Gbg
...
```

**Format:**
- Jeder Wochentag beginnt mit dem Wochentag-Namen
- Stunden im Format: `Stunde X = Lehrerkürzel`
- Freistunden mit `None` markieren

## Verwendung 💻

### Einmalige Ausführung

```bash
python vertretungsplan_scraper.py
```

Das Programm fragt nach:
- Benutzername (Schulportal)
- Passwort
- Institutions-ID (Standard: 6081)

### Ausgabe-Beispiel

```
======================================================================
STUNDENPLAN-ABGLEICH
======================================================================

📅 Prüfe Montag, 02.12.2025
   🚨 NEUER AUSFALL: Stunde 5 (Urc) fällt aus!
   🚨 NEUER AUSFALL: Stunde 6 (Urc) fällt aus!

📅 Prüfe Dienstag, 03.12.2025
   🔄 [DEBUG] Bereits bekannt: Stunde 1 (Nie) fällt aus
   ✅ Keine neuen Ausfälle

======================================================================
ZUSAMMENFASSUNG
======================================================================
🆕 Neue Ausfälle: 2
🔄 Bereits bekannte Ausfälle: 1
📊 Gesamt: 3
======================================================================
```

## Wie es funktioniert 🔧

1. **Login**: Automatischer Login ins Schulportal Hessen
2. **Abruf**: Vertretungsplan wird von der Webseite geladen
3. **Parsing**: HTML wird geparst und in strukturierte Daten umgewandelt
4. **Abgleich**: 
   - Dein Stundenplan wird mit dem Vertretungsplan abgeglichen
   - Nur Ausfälle bei DEINEN Lehrern werden erkannt
   - Nur Stunden, die du auch hast, werden geprüft
5. **Tracking**: 
   - Neue Ausfälle werden in `known_ausfaelle.json` gespeichert
   - Beim nächsten Durchlauf werden bereits bekannte Ausfälle als [DEBUG] markiert
6. **Benachrichtigung**: Klare Meldung neuer Ausfälle in der Konsole

## Roadmap 🗺️

### Phase 1: Basis-Funktionalität ✅ (AKTUELL)
- [x] Login und Vertretungsplan-Abruf
- [x] Stundenplan-Parser
- [x] Abgleich-Logik
- [x] Tracking bereits gemeldeter Ausfälle
- [x] Konsolen-Output

### Phase 2: Automatisierung 🔜 (NEXT)
- [ ] Automatische Ausführung alle 5 Minuten
- [ ] Discord Webhook Integration
- [ ] Benachrichtigung nur bei neuen Ausfällen
- [ ] Systemd Service / Windows Task Scheduler Setup

### Phase 3: Erweiterungen 💡 (FUTURE)
- [ ] Web-Interface
- [ ] Mehrere Stundenpläne unterstützen
- [ ] Email-Benachrichtigungen
- [ ] Telegram Bot Integration
- [ ] Mobile App

## Troubleshooting 🔍

### Browser startet nicht
```bash
playwright install chrome
```

### Encoding-Fehler
Stelle sicher, dass alle Dateien in UTF-8 kodiert sind.

### Login schlägt fehl
- Überprüfe Benutzername und Passwort
- Prüfe die Institutions-ID (meist 4-stellig)

## Sicherheitshinweise 🔒

- ⚠️ Speichere niemals deine Login-Daten im Code!
- ⚠️ Committe keine Dateien mit Passwörtern ins Git-Repo
- 💡 Nutze später Umgebungsvariablen für Credentials

## Contributing 🤝

Contributions sind willkommen! Bitte erstelle einen Pull Request.

## Lizenz 📄

MIT License - Frei verwendbar für private und schulische Zwecke.

## Kontakt 📧

Bei Fragen oder Problemen erstelle ein Issue im Repository.

---

**Hinweis**: Dieses Projekt ist für private/schulische Nutzung gedacht und steht nicht in Verbindung mit dem offiziellen Schulportal Hessen.
