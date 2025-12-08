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

## ✅ Schritt 3: Python & Git installieren

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

## ✅ Schritt 5: Setup ausführbar machen

```bash
chmod +x setup.sh
```

---

## ✅ Schritt 6: Setup starten

```bash
./setup.sh
```

**Jetzt wirst du gefragt nach:**
1. Discord Bot Token
2. Discord User ID
3. Institution (Enter für 6081)
4. Check-Intervall (Enter für 5 Min)
5. Stats-Intervall (Enter für 1 Std)

---

## ✅ Schritt 7: Bot starten

```bash
python3 discord_bot.py
```

**Du siehst:**
- "Bot eingeloggt als..."
- Bekommst Discord DM: "✅ Vertretungsplan Bot ist bereit!"

---

## ✅ Schritt 8: In Discord

1. Öffne Discord
2. Gehe zu DMs mit dem Bot
3. Schreibe: `/start`
4. Gib ein:
   - Schulportal Benutzername
   - Schulportal Passwort
   - Institution (Enter für 6081)

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

# === Setup ===
chmod +x setup.sh
./setup.sh

# === Bot starten ===
python3 discord_bot.py
```

---

## 🔄 Zusätzliche Commands

### Bot stoppen
```bash
Ctrl + C
```

### Bot im Hintergrund (Screen)
```bash
# Screen installieren
sudo apt install screen -y

# Screen starten
screen -S bot

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
python3 discord_bot.py
```

### Logs anzeigen
```bash
tail -f bot.log
```

### Projekt löschen (falls nötig)
```bash
cd ~
rm -rf Schulportal_Project
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

### Chromium-Fehler
```bash
playwright install chromium
playwright install-deps chromium
```

### Bot verbindet nicht
```bash
# .env prüfen
cat .env

# Token muss mit MTQ... beginnen
# Neu bearbeiten:
nano .env
```

---

**Das wars! Bei Fragen siehe:**
- [WSL_INSTALLATION_GUIDE.md](WSL_INSTALLATION_GUIDE.md)
- [DISCORD_BOT_GUIDE.md](DISCORD_BOT_GUIDE.md)
- GitHub Issues erstellen
