# Windows WSL Installation Guide 🪟🐧

**Vollständige Schritt-für-Schritt Anleitung für Windows mit WSL (Ubuntu)**

---

## Teil 1: WSL Installation und Vorbereitung

### Schritt 1: WSL installieren (falls noch nicht installiert)

```powershell
# PowerShell als Administrator öffnen
wsl --install
```

**Nach Installation:** Computer neu starten

### Schritt 2: Ubuntu starten

```powershell
# Ubuntu starten
wsl
```

Beim ersten Start wirst du nach Username und Passwort gefragt.

### Schritt 3: System aktualisieren

```bash
sudo apt update
sudo apt upgrade -y
```

---

## Teil 2: Python und Git installieren

### Schritt 4: Python 3 installieren

```bash
sudo apt install python3 python3-pip python3-venv -y
```

**Prüfe Installation:**
```bash
python3 --version
# Sollte: Python 3.x.x anzeigen
```

### Schritt 5: Git installieren

```bash
sudo apt install git -y
```

**Prüfe Installation:**
```bash
git --version
# Sollte: git version x.x.x anzeigen
```

---

## Teil 3: Repository klonen und einrichten

### Schritt 6: Ins Home-Verzeichnis wechseln

```bash
cd ~
```

### Schritt 7: Repository klonen

```bash
git clone https://github.com/Miggo65/Schulportal_Project.git
```

### Schritt 8: Ins Projektverzeichnis wechseln

```bash
cd Schulportal_Project
```

### Schritt 9: Setup-Skript ausführbar machen

```bash
chmod +x setup.sh
```

---

## Teil 4: Automatisches Setup ausführen

### Schritt 10: Setup starten

```bash
./setup.sh
```

**Das Skript fragt dich interaktiv nach:**

1. **Discord Bot Token**
   - Gehe zu: https://discord.com/developers/applications
   - Wähle deine App → Bot → Reset Token (falls noch nicht geschehen)
   - Kopiere das Token
   - Füge es ein (wird nicht angezeigt beim Tippen!)

2. **Discord User ID**
   - Discord öffnen
   - Einstellungen → Erweitert → Entwicklermodus aktivieren
   - Rechtsklick auf dich selbst → ID kopieren
   - Füge die ID ein

3. **Institutions-ID** (Optional)
   - Standard: 6081
   - Einfach Enter drücken für Standard

4. **Check-Intervall** (Optional)
   - Standard: 300 (5 Minuten)
   - Einfach Enter drücken für Standard

5. **Statistik-Intervall** (Optional)
   - Standard: 3600 (1 Stunde)
   - Einfach Enter drücken für Standard

**Das Skript installiert automatisch:**
- ✅ Python Dependencies
- ✅ Chromium Browser
- ✅ Erstellt .env Datei mit deinen Eingaben

---

## Teil 5: Bot starten

### Schritt 11: Discord Bot starten

```bash
python3 discord_bot.py
```

**Was jetzt passiert:**

1. Bot startet und verbindet sich mit Discord
2. Du bekommst eine DM: **"✅ Vertretungsplan Bot ist bereit!"**
3. Schreibe in die DM: `/start`
4. Bot fragt nach:
   - Schulportal Benutzername
   - Schulportal Passwort (wird nach Eingabe gelöscht)
   - Institutions-ID (Optional, Enter für Standard)
5. Bot beginnt mit dem Monitoring!

---

## Zusammenfassung: Alle Commands in Reihenfolge

```bash
# 1. WSL starten (PowerShell/CMD)
wsl

# 2. System aktualisieren
sudo apt update && sudo apt upgrade -y

# 3. Python und Git installieren
sudo apt install python3 python3-pip python3-venv git -y

# 4. Repository klonen
cd ~
git clone https://github.com/Miggo65/Schulportal_Project.git

# 5. Ins Projektverzeichnis
cd Schulportal_Project

# 6. Setup ausführbar machen
chmod +x setup.sh

# 7. Setup starten (fragt nach Token, User ID, etc.)
./setup.sh

# 8. Bot starten
python3 discord_bot.py
```

---

## Zusätzliche Befehle

### Bot stoppen

```bash
# Im Terminal wo der Bot läuft:
Ctrl + C
```

### Bot im Hintergrund laufen lassen (Screen)

```bash
# Screen installieren
sudo apt install screen -y

# Screen-Session starten
screen -S schulportal-bot

# Bot starten
python3 discord_bot.py

# Session verlassen (Bot läuft weiter)
Ctrl + A, dann D

# Zurück zur Session
screen -r schulportal-bot

# Session beenden
exit
```

### Repository aktualisieren (bei Updates)

```bash
cd ~/Schulportal_Project
git pull
./setup.sh  # Falls nötig
python3 discord_bot.py
```

### Logs anzeigen

```bash
# Live-Logs
tail -f bot.log

# Letzte 50 Zeilen
tail -n 50 bot.log
```

---

## Troubleshooting

### WSL startet nicht

**PowerShell als Admin:**
```powershell
# WSL Feature aktivieren
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Computer neu starten
```

### Python nicht gefunden

```bash
# Alternative Python Installation
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip -y
```

### Chromium Installation schlägt fehl

```bash
# System-Dependencies installieren
sudo apt install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2

# Playwright neu installieren
playwright install chromium
playwright install-deps chromium
```

### Permission Denied bei setup.sh

```bash
# Ausführbar machen
chmod +x setup.sh

# Falls immer noch Fehler:
bash setup.sh
```

### Discord Bot verbindet nicht

**Prüfe .env:**
```bash
cat .env
# Token muss mit MTQ... beginnen
# Keine Leerzeichen vor/nach Token
```

**Token neu eingeben:**
```bash
nano .env
# Bearbeite DISCORD_BOT_TOKEN=...
# Speichern: Ctrl+O, Enter, Ctrl+X
```

---

## Für Ubuntu Server (ohne WSL)

**Gleiche Commands, aber:**

```bash
# 1. Per SSH einloggen
ssh user@server-ip

# 2. Ab Schritt 2 weitermachen (System aktualisieren)
sudo apt update && sudo apt upgrade -y
# ... rest wie oben
```

---

## Autostart einrichten (Optional)

### Mit Systemd (für 24/7 Betrieb)

```bash
# Service-Datei erstellen
sudo nano /etc/systemd/system/schulportal-bot.service
```

**Inhalt:**
```ini
[Unit]
Description=Schulportal Discord Bot
After=network.target

[Service]
Type=simple
User=DEIN_USERNAME
WorkingDirectory=/home/DEIN_USERNAME/Schulportal_Project
ExecStart=/usr/bin/python3 /home/DEIN_USERNAME/Schulportal_Project/discord_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Aktivieren:**
```bash
# Service aktivieren
sudo systemctl daemon-reload
sudo systemctl enable schulportal-bot
sudo systemctl start schulportal-bot

# Status prüfen
sudo systemctl status schulportal-bot

# Logs anzeigen
sudo journalctl -u schulportal-bot -f
```

---

## Status prüfen

```bash
# Bot läuft?
ps aux | grep discord_bot.py

# Prozess killen (falls nötig)
pkill -f discord_bot.py
```

---

**Das wars! Der Bot sollte jetzt laufen und dich bei neuen Ausfällen benachrichtigen.** 🎉
