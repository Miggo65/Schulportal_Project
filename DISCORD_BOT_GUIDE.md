# Discord Bot Setup & Verwendung 🤖

## ⚠️ WICHTIG - Sicherheit zuerst!

**NIEMALS** dein Bot Token öffentlich posten oder committen! Wenn du es versehentlich geteilt hast:

1. Gehe zu https://discord.com/developers/applications
2. Wähle deine App
3. Bot → Reset Token
4. Generiere ein neues Token

## 📋 Setup-Schritte

### 1. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 2. .env Datei erstellen

Kopiere `.env.example` zu `.env`:

```bash
cp .env.example .env
```

Bearbeite `.env` und füge dein **NEUES** Bot Token ein:

```env
DISCORD_BOT_TOKEN=DEIN_NEUES_TOKEN_HIER
DISCORD_USER_ID=993180608614383637
SCHULPORTAL_INSTITUTION=6081
CHECK_INTERVAL=300
STATS_INTERVAL=3600
```

### 3. Bot Permissions einrichten

Dein Bot braucht folgende Permissions in Discord:
- ✅ Send Messages
- ✅ Embed Links
- ✅ Read Message History

**Invite Link generieren:**
1. Gehe zu https://discord.com/developers/applications
2. Wähle deine App → OAuth2 → URL Generator
3. Scopes: `bot`
4. Bot Permissions: `Send Messages`, `Embed Links`, `Read Message History`
5. Kopiere den Link und öffne ihn im Browser
6. Füge den Bot zu deinem Server hinzu

### 4. Bot starten

```bash
python discord_bot.py
```

## 🎮 Commands

### `/start`
Startet das Monitoring. Der Bot fragt nach:
1. **Benutzername** (Schulportal)
2. **Passwort** (wird nach Eingabe gelöscht)
3. **Institutions-ID** (Optional, Standard: 6081)

Danach:
- ✅ Prüft alle 5 Minuten auf neue Ausfälle
- 📊 Sendet stündlich eine Statistik
- 🚨 Benachrichtigt sofort bei neuen Ausfällen

### `/stop`
Stoppt das Monitoring.

### `/status`
Zeigt den aktuellen Status und Statistiken:
- Anzahl erfolgreicher/fehlgeschlagener Scans
- Gefundene Ausfälle
- Letzter Scan-Zeitpunkt

## 📱 Bot Verwendung

### Initial Setup

1. Starte den Bot mit `python discord_bot.py`
2. Du erhältst eine DM: **"✅ Vertretungsplan Bot ist bereit!"**
3. Schreibe `/start` in die DM
4. Gib deine Schulportal-Credentials ein
5. Bot beginnt mit dem Monitoring!

### Ausgaben

**Bei neuen Ausfällen:**
```
🚨 NEUER AUSFALL!

📅 Datum: Montag, 09.12.2025
⏰ Stunde: 5
👨‍🏫 Lehrer: Urc

Scan #42
```

**Stündliche Statistik:**
```
📊 Stündliche Statistik

Erfolgreiche Scans: 12
Fehlgeschlagene Scans: 0
Neue Ausfälle gefunden: 3
Letzter Scan: 14:35:42
```

## 🔧 Konfiguration

### Intervalle anpassen

In `.env`:
```env
CHECK_INTERVAL=300      # Sekunden (5 Minuten)
STATS_INTERVAL=3600     # Sekunden (1 Stunde)
```

**Empfohlene Werte:**
- `CHECK_INTERVAL`: 300 (5 Min) bis 600 (10 Min)
- `STATS_INTERVAL`: 3600 (1 Std) bis 7200 (2 Std)

⚠️ Zu häufige Checks könnten vom Schulportal blockiert werden!

## 📊 Logs

Der Bot erstellt automatisch `bot.log` mit detaillierten Logs:

```bash
# Logs in Echtzeit anzeigen
tail -f bot.log

# Letzte 50 Zeilen
tail -n 50 bot.log
```

## 🐛 Troubleshooting

### Bot sendet keine DM

**Problem:** "Cannot send messages to this user"

**Lösung:**
1. Discord → Einstellungen → Privatsphäre & Sicherheit
2. ✅ Aktiviere "Direktnachrichten von Servermitgliedern zulassen"

### Bot verbindet nicht

**Fehler:** `discord.errors.LoginFailure`

**Lösung:**
- Token in `.env` überprüfen
- Kein Leerzeichen vor/nach dem Token
- Token muss mit `MTQ...` beginnen

### Playwright-Fehler

```bash
# Browser neu installieren
playwright install chromium
playwright install-deps chromium  # Nur Linux
```

### Login schlägt fehl

**Mögliche Ursachen:**
- Falsche Credentials
- Schulportal nicht erreichbar
- Captcha/2FA aktiviert (noch nicht unterstützt)

**Debug:**
```bash
# Teste Login manuell
python vertretungsplan_scraper.py
```

## 🚀 Produktiv-Betrieb

### Linux mit Systemd

Erstelle `/etc/systemd/system/schulportal-bot.service`:

```ini
[Unit]
Description=Schulportal Vertretungsplan Discord Bot
After=network.target

[Service]
Type=simple
User=deinuser
WorkingDirectory=/pfad/zu/Schulportal_Project
ExecStart=/usr/bin/python3 /pfad/zu/Schulportal_Project/discord_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable schulportal-bot
sudo systemctl start schulportal-bot
sudo systemctl status schulportal-bot
```

### Windows

1. Erstelle `start_bot.bat`:
```batch
@echo off
cd /d %~dp0
python discord_bot.py
pause
```

2. Task Scheduler:
   - Trigger: Bei Systemstart
   - Aktion: `start_bot.bat` ausführen

### macOS

Erstelle `~/Library/LaunchAgents/com.schulportal.bot.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.schulportal.bot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/pfad/zu/discord_bot.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>/pfad/zu/Schulportal_Project</string>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.schulportal.bot.plist
```

## 📝 Best Practices

1. **Sicherheit:**
   - Niemals `.env` committen
   - Token regelmäßig erneuern
   - Passwort nicht im Code speichern

2. **Monitoring:**
   - Logs regelmäßig prüfen
   - Bei vielen Fehlern: Intervall erhöhen
   - Stundenplan aktuell halten

3. **Performance:**
   - Bot auf Server/Raspberry Pi laufen lassen
   - Nicht auf Laptop (muss immer an sein)
   - Stabile Internetverbindung

## 🆘 Support

Bei Problemen:
1. Prüfe `bot.log`
2. Teste mit `/status`
3. Erstelle ein Issue im GitHub Repo mit:
   - Fehlermeldung
   - Relevante Log-Zeilen
   - Bot Status

---

**Viel Erfolg mit deinem Vertretungsplan-Bot!** 🎉
