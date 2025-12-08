# Schulportal Vertretungsplan Bot 🏫🤖

**Automatischer Discord Bot für Vertretungsplan-Benachrichtigungen**

Prüft alle 5 Minuten den Schulportal Hessen Vertretungsplan und sendet dir sofort eine Discord-Nachricht bei neuen Ausfällen in deinem Stundenplan.

---

## 🚀 Quick Start (Windows WSL / Ubuntu)

### Einmalige Einrichtung

```bash
# 1. WSL starten (PowerShell/CMD)
wsl

# 2. System vorbereiten
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git -y

# 3. Repository klonen
cd ~
git clone https://github.com/Miggo65/Schulportal_Project.git
cd Schulportal_Project

# 4. Setup starten (fragt nach Token, User ID, etc.)
chmod +x setup.sh
./setup.sh

# 5. Bot starten
python3 discord_bot.py
```

**Das wars!** Der Bot fragt dich nach Schulportal-Login und beginnt mit dem Monitoring.

---

## 📚 Ausführliche Anleitungen

- **[Windows WSL Installation](WSL_INSTALLATION_GUIDE.md)** - Vollständige Schritt-für-Schritt Anleitung
- **[Discord Bot Guide](DISCORD_BOT_GUIDE.md)** - Erweiterte Features & Konfiguration

---

## ✨ Features

- ✅ Automatische Prüfung alle 5 Minuten
- ✅ Sofort-Benachrichtigung bei neuen Ausfällen
- ✅ Nur relevante Ausfälle (deine Lehrer, deine Stunden)
- ✅ Stündliche Statistik
- ✅ Tracking verhindert Duplikate
- ✅ Sicherer Login (Passwort wird nicht gespeichert)

---

## 🎮 Commands

Nach dem Start in Discord DM:

- `/start` - Monitoring starten (fragt nach Schulportal-Login)
- `/stop` - Monitoring stoppen
- `/status` - Status & Statistiken anzeigen

---

## 📱 Beispiel-Ausgaben

### Neue Ausfälle
```
🚨 NEUER AUSFALL!

📅 Datum: Montag, 09.12.2025
⏰ Stunde: 5
👨‍🏫 Lehrer: Urc

Scan #42
```

### Stündliche Statistik
```
📊 Stündliche Statistik

Erfolgreiche Scans: 12
Fehlgeschlagene Scans: 0
Neue Ausfälle gefunden: 3
```

---

## 🔧 Konfiguration

Die Konfiguration erfolgt beim ersten `./setup.sh` Lauf:

- **Discord Bot Token** - Von https://discord.com/developers/applications
- **Discord User ID** - Rechtsklick auf dich in Discord → ID kopieren
- **Check-Intervall** - Standard: 300 Sekunden (5 Min)
- **Stats-Intervall** - Standard: 3600 Sekunden (1 Std)

---

## 📁 Projektstruktur

```
Schulportal_Project/
├── discord_bot.py              # Discord Bot (Hauptprogramm)
├── schulportal_lib.py          # Schulportal API
├── stundenplan_checker.py      # Abgleich-Logik
├── Stundenplan.txt             # DEIN Stundenplan (anpassen!)
├── setup.sh                    # Interaktives Setup
├── requirements.txt            # Python Dependencies
└── .env                        # Config (wird von setup.sh erstellt)
```

---

## 🐛 Troubleshooting

### Bot sendet keine DM
Discord → Einstellungen → Privatsphäre & Sicherheit  
✅ "Direktnachrichten von Servermitgliedern zulassen"

### Login schlägt fehl
```bash
# Teste Login manuell
python3 vertretungsplan_scraper.py
```

### Bot verbindet nicht
```bash
# .env prüfen
cat .env
# Token muss mit MTQ... beginnen
```

### Chromium-Fehler
```bash
playwright install chromium
playwright install-deps chromium
```

---

## 🔄 Updates

```bash
cd ~/Schulportal_Project
git pull
./setup.sh  # Falls neue Config-Optionen hinzugekommen sind
python3 discord_bot.py
```

---

## 🔒 Sicherheit

- ⚠️ **Bot Token niemals public posten!**
- ⚠️ `.env` niemals committen!
- ✅ Passwort wird nur im RAM gespeichert, nie auf Disk
- ✅ Passwort-Nachricht wird nach Eingabe gelöscht

---

## 📊 24/7 Betrieb

### Screen (einfach)
```bash
# Screen installieren
sudo apt install screen -y

# Session starten
screen -S schulportal-bot
python3 discord_bot.py

# Session verlassen: Ctrl+A, dann D
# Zurückkehren: screen -r schulportal-bot
```

### Systemd (professionell)
Siehe [Discord Bot Guide](DISCORD_BOT_GUIDE.md) für Systemd-Service Einrichtung.

---

## 🤝 Support

Bei Problemen:
1. Prüfe `bot.log`
2. Nutze `/status` Command
3. Siehe [WSL_INSTALLATION_GUIDE.md](WSL_INSTALLATION_GUIDE.md)
4. Erstelle ein GitHub Issue

---

## 📝 Dateien zum Löschen

Nach erfolgreichem Setup kannst du folgende Dateien löschen:

```bash
rm test_checker.py
rm vertretungsplan_scraper.py  # Wird vom Bot nicht benötigt
rm -rf Vertretungsplan_saves    # Alte Test-Daten
rm -rf __pycache__              # Python Cache
```

---

## 🎯 Roadmap

- [x] Stundenplan-Abgleich
- [x] Discord Bot
- [x] Automatisches Monitoring
- [x] Tracking-System
- [ ] Web-Interface
- [ ] Multi-User Support
- [ ] Telegram Bot Alternative

---

**Entwickelt mit ❤️ für Schüler die keine Ausfälle verpassen wollen!**

MIT License - Frei verwendbar für private und schulische Zwecke.
