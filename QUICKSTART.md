# 🚀 QUICK START - Alle Commands in Reihenfolge

**Kopiere diese Commands einfach nacheinander in dein Terminal!**

---

## ✅ Schritt 1: WSL starten

```powershell
# In PowerShell oder CMD (Windows)
wsl
```

---

## ✅ Schritt 2: System aktualisieren

```bash
sudo apt update && sudo apt upgrade -y
```

---

## ✅ Schritt 3: Python, Git & Dependencies installieren

```bash
sudo apt install python3 python3-pip python3-venv git -y
```

---

## ✅ Schritt 4: Repository klonen

```bash
cd ~
git clone https://github.com/Miggo65/Schulportal_Project.git
cd Schulportal_Project
```

---

## ✅ Schritt 5: Virtual Environment erstellen

```bash
python3 -m venv venv
source venv/bin/activate
```

**Wichtig:** Ab jetzt alle Commands im venv ausführen!

---

## ✅ Schritt 6: Setup ausführbar machen

```bash
chmod +x setup.sh
```

---

## ✅ Schritt 7: Setup starten

```bash
./setup.sh
```

**Jetzt wirst du gefragt nach:**
1. Discord Bot Token
2. Discord User ID
3. Optional: Schulportal Credentials (oder später beim /start)
4. Institution (Enter für 6081)
5. Check-Intervall (Enter für 5 Min)

---

## ✅ Schritt 8: Bot starten

```bash
python3 discord_bot.py
```

**Du siehst:**
- "Bot eingeloggt als..."
- Bekommst Discord DM: "✅ Vertretungsplan Bot ist bereit!"

---

## ✅ Schritt 9: In Discord

1. Öffne Discord
2. Gehe zu DMs mit dem Bot
3. Schreibe: `/start`
4. Gib ein:
   - Schulportal Benutzername (oder `.` für Standard aus .env)
   - Schulportal Passwort als Spoiler: `||deinPasswort||` (oder `.` für Standard)
   - Institution (`.` für Standard)

**Fertig!** Bot läuft jetzt! 🎉

---

## 📋 Komplett-Liste (Copy & Paste)

```bash
# === WSL/Ubuntu vorbereiten ===
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git -y

# === Repository klonen ===
cd ~
git clone https://github.com/Miggo65/Schulportal_Project.git
cd Schulportal_Project

# === Virtual Environment ===
python3 -m venv venv
source venv/bin/activate

# === Setup ===
chmod +x setup.sh
./setup.sh

# === Bot starten ===
python3 discord_bot.py
```

---

## 🎮 Discord Commands

### `/start`
Startet das Monitoring.

**Eingaben:**
- Benutzername: Dein Schulportal-Username (oder `.` für .env)
- Passwort: `||deinPasswort||` mit Spoiler-Tags! (oder `.` für .env)
- Institution: `.` für Standard (6081)

### `/stop`
Stoppt das Monitoring.

### `/scanstatus`
Zeigt Status und Statistiken:
- Anzahl erfolgreicher/fehlgeschlagener Scans
- Gefundene Ausfälle
- Letzter Scan-Zeitpunkt

---

## 🔄 Zusätzliche Commands

### Bot stoppen
```bash
Ctrl + C
```

### Aus venv ausloggen
```bash
deactivate
```

### Wieder in venv einloggen
```bash
cd ~/Schulportal_Project
source venv/bin/activate
```

### Bot im Hintergrund (Screen)
```bash
# Screen installieren
sudo apt install screen -y

# Screen starten
screen -S bot

# venv aktivieren
source venv/bin/activate

# Bot starten
python3 discord_bot.py

# Screen verlassen (Bot läuft weiter)
Ctrl + A, dann D

# Zurück zum Bot
screen -r bot
```

### Updates holen
```bash
cd ~/Schulportal_Project
git pull
source venv/bin/activate  # Falls nicht schon aktiv
python3 discord_bot.py
```

### Logs anzeigen
```bash
tail -f bot.log
```

### Chromium neu installieren (bei Problemen)
```bash
source venv/bin/activate
python3 -m playwright install-deps
python3 -m playwright install chromium
```

---

## 🧹 Aufräumen (Optional)

Nach erfolgreichem Test:

```bash
cd ~/Schulportal_Project

# Unnötige Dateien löschen
rm test_checker.py
rm vertretungsplan_scraper.py
rm -rf __pycache__
rm -rf Vertretungsplan_saves
mkdir Vertretungsplan_saves
```

---

## ⚠️ Troubleshooting

### WSL startet nicht
```powershell
# PowerShell als Administrator
wsl --install
# Computer neu starten
```

### Python-Fehler
```bash
# Python Version prüfen
python3 --version
# Sollte 3.8+ sein
```

### playwright: command not found
```bash
# WICHTIG: Nutze python3 -m prefix
python3 -m playwright install chromium
python3 -m playwright install-deps
```

### Bot verbindet nicht
```bash
# .env prüfen
cat .env
# Token muss mit MTQ... oder ähnlich beginnen
```

### "libasound2t64 not found"
```bash
# Für ältere Ubuntu-Versionen
sudo apt install libasound2 -y
```

### Chromium startet nicht
```bash
# System-Dependencies neu installieren
sudo apt update
sudo apt install -y libnss3 libnspr4 libasound2t64
python3 -m playwright install-deps
python3 -m playwright install chromium
```

---

## 💡 Tipps

### Passwort sicher eingeben in Discord
Schreibe es immer mit Spoiler-Tags:
```
||deinPasswort||
```
Das wird dann als Spoiler angezeigt und nur sichtbar wenn man draufklickt.

### Standard-Werte nutzen
Wenn du beim Setup Schulportal-Credentials in .env gespeichert hast:
- Beim `/start` Command einfach `.` eingeben
- Bot nutzt dann die Werte aus .env

### Screen für 24/7 Betrieb
Screen ist perfekt für WSL/Ubuntu:
```bash
screen -S bot
source venv/bin/activate
python3 discord_bot.py
# Ctrl+A, D zum Verlassen
```

---

**Das wars! Bei Fragen siehe:**
- [WSL_INSTALLATION_GUIDE.md](WSL_INSTALLATION_GUIDE.md)
- [DISCORD_BOT_GUIDE.md](DISCORD_BOT_GUIDE.md)
- GitHub Issues erstellen
