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

### Schritt 4: Python 3, venv und Git installieren

```bash
sudo apt install python3 python3-pip python3-venv git -y
```

**Prüfe Installation:**
```bash
python3 --version
# Sollte: Python 3.x.x anzeigen
```

---

## Teil 3: Repository klonen und Virtual Environment

### Schritt 5: Ins Home-Verzeichnis wechseln

```bash
cd ~
```

### Schritt 6: Repository klonen

```bash
git clone https://github.com/Miggo65/Schulportal_Project.git
```

### Schritt 7: Ins Projektverzeichnis wechseln

```bash
cd Schulportal_Project
```

### Schritt 8: Virtual Environment erstellen und aktivieren

```bash
# venv erstellen
python3 -m venv venv

# venv aktivieren
source venv/bin/activate
```

**Du siehst jetzt `(venv)` vor deinem Prompt!**

---

## Teil 4: Setup ausführen

### Schritt 9: Setup-Skript ausführbar machen

```bash
chmod +x setup.sh
```

### Schritt 10: Setup starten

```bash
./setup.sh
```

**Das Skript macht automatisch:**
1. ✅ Installiert Python Dependencies
2. ✅ Installiert System-Dependencies (libnss3, libnspr4, libasound2t64)
3. ✅ Installiert Playwright Dependencies mit `python3 -m playwright install-deps`
4. ✅ Installiert Chromium mit `python3 -m playwright install chromium`

**Und fragt dich nach:**
1. **Discord Bot Token**
   - Gehe zu: https://discord.com/developers/applications
   - Wähle deine App → Bot → Copy Token
   - Füge es ein

2. **Discord User ID**
   - Discord öffnen
   - Einstellungen → Erweitert → Entwicklermodus aktivieren
   - Rechtsklick auf dich selbst → ID kopieren

3. **Optional: Schulportal Credentials**
   - Du kannst sie jetzt speichern (j) oder später beim `/start` eingeben (n)
   - Falls ja: Benutzername und Passwort

4. **Institutions-ID** (Optional)
   - Standard: 6081
   - Enter für Standard

5. **Check-Intervall** (Optional)
   - Standard: 300 (5 Minuten)
   - Enter für Standard

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
   - Schulportal Benutzername (oder `.` für .env)
   - Schulportal Passwort: **`||deinPasswort||`** (mit Spoiler-Tags!) oder `.` für .env
   - Institutions-ID (`.` für Standard)
5. Bot beginnt mit dem Monitoring!

---

## Zusammenfassung: Alle Commands in Reihenfolge

```bash
# 1. WSL starten (PowerShell/CMD)
wsl

# 2. System aktualisieren
sudo apt update && sudo apt upgrade -y

# 3. Python, venv und Git installieren
sudo apt install python3 python3-pip python3-venv git -y

# 4. Repository klonen
cd ~
git clone https://github.com/Miggo65/Schulportal_Project.git

# 5. Ins Projektverzeichnis
cd Schulportal_Project

# 6. Virtual Environment erstellen und aktivieren
python3 -m venv venv
source venv/bin/activate

# 7. Setup ausführbar machen
chmod +x setup.sh

# 8. Setup starten (fragt nach Token, User ID, etc.)
./setup.sh

# 9. Bot starten
python3 discord_bot.py
```

---

## Discord Commands

### `/start`
Startet Monitoring. Du musst eingeben:
- Benutzername (oder `.` für .env)
- Passwort als Spoiler: `||passwort||` (oder `.` für .env)
- Institution (`.` für Standard)

### `/stop`
Stoppt Monitoring

### `/scanstatus`
Zeigt Status und Statistiken

---

## Zusätzliche Befehle

### Bot stoppen

```bash
# Im Terminal wo der Bot läuft:
Ctrl + C
```

### Virtual Environment

```bash
# venv aktivieren (falls nicht aktiv)
source venv/bin/activate

# venv deaktivieren
deactivate
```

### Bot im Hintergrund laufen lassen (Screen)

```bash
# Screen installieren
sudo apt install screen -y

# Screen-Session starten
screen -S schulportal-bot

# venv aktivieren
source venv/bin/activate

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
source venv/bin/activate  # Falls nicht schon aktiv
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

### playwright: command not found

```bash
# WICHTIG: Nutze python3 -m prefix!
python3 -m playwright install chromium
python3 -m playwright install-deps
```

### Chromium Installation schlägt fehl

```bash
# System-Dependencies manuell installieren
sudo apt update
sudo apt install -y libnss3 libnspr4 libasound2t64

# Für ältere Ubuntu-Versionen
sudo apt install -y libasound2

# Playwright neu installieren
python3 -m playwright install-deps
python3 -m playwright install chromium
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
# Token muss mit MTQ... oder ähnlich beginnen
# Keine Leerzeichen vor/nach Token
```

**Token neu eingeben:**
```bash
nano .env
# Bearbeite DISCORD_BOT_TOKEN=...
# Speichern: Ctrl+O, Enter, Ctrl+X
```

### "Cannot send empty message" in Discord

Discord erlaubt keine leeren Nachrichten. Deshalb:
- Statt Enter für Standard → sende `.` (Punkt)
- Passwort mit Spoiler-Tags: `||deinPasswort||`

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
Environment="PATH=/home/DEIN_USERNAME/Schulportal_Project/venv/bin:/usr/bin"
ExecStart=/home/DEIN_USERNAME/Schulportal_Project/venv/bin/python3 /home/DEIN_USERNAME/Schulportal_Project/discord_bot.py
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

## 💡 Wichtige Tipps

### Virtual Environment immer aktivieren!
```bash
cd ~/Schulportal_Project
source venv/bin/activate
# Jetzt siehst du (venv) vor dem Prompt
```

### Playwright nur mit python3 -m
```bash
# RICHTIG:
python3 -m playwright install chromium

# FALSCH:
playwright install chromium  # Funktioniert nicht in venv!
```

### Passwort sicher in Discord
Immer mit Spoiler-Tags schreiben:
```
||meinPasswort123||
```

### Standard-Werte nutzen
Beim `/start` Command `.` eingeben um Werte aus .env zu nutzen.

---

**Das wars! Der Bot sollte jetzt laufen und dich bei neuen Ausfällen benachrichtigen.** 🎉
