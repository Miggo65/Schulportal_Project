#!/bin/bash

# Schulportal Discord Bot - Interaktives Setup
# Dieses Skript führt durch die komplette Einrichtung

set -e  # Beende bei Fehler

echo "=========================================="
echo "Schulportal Discord Bot - Setup"
echo "=========================================="
echo ""

# Check Python
echo "🔍 Prüfe Python Installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 nicht gefunden!"
    echo "Installiere Python 3.8 oder höher:"
    echo "  sudo apt update"
    echo "  sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION gefunden"
echo ""

# Prüfe ob wir in venv sind
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  WARNUNG: Nicht in Virtual Environment!"
    echo "Es wird empfohlen ein venv zu verwenden."
    echo ""
    read -p "Trotzdem fortfahren? (j/n): " continue_anyway
    if [ "$continue_anyway" != "j" ]; then
        echo "Abgebrochen. Erstelle zuerst ein venv:"
        echo "  python3 -m venv venv"
        echo "  source venv/bin/activate"
        exit 1
    fi
fi

# Dependencies installieren
echo "📦 Installiere Python Dependencies..."
pip install -r requirements.txt -q

if [ $? -ne 0 ]; then
    echo "❌ Fehler beim Installieren der Dependencies!"
    exit 1
fi

echo "✅ Dependencies installiert"
echo ""

# System-Dependencies für Playwright (WSL/Ubuntu)
echo "🔧 Installiere System-Dependencies für Playwright..."
sudo apt update
sudo apt install -y libnss3 libnspr4 libasound2t64

if [ $? -ne 0 ]; then
    echo "⚠️  Fehler bei System-Dependencies (optional)"
    echo "Versuche trotzdem fortzufahren..."
fi

echo "✅ System-Dependencies installiert"
echo ""

# Playwright Browser installieren
echo "🌐 Installiere Chromium Browser..."
python3 -m playwright install-deps
python3 -m playwright install chromium

if [ $? -ne 0 ]; then
    echo "❌ Fehler beim Installieren von Chromium!"
    echo "Versuche manuell:"
    echo "  python3 -m playwright install-deps"
    echo "  python3 -m playwright install chromium"
    exit 1
fi

echo "✅ Chromium installiert"
echo ""

# Interaktive .env Erstellung
echo "=========================================="
echo "📝 Konfiguration"
echo "=========================================="
echo ""

# Frage nach Discord Bot Token
echo "🤖 Bitte gib dein Discord Bot Token ein:"
echo "   (Token erhältst du von: https://discord.com/developers/applications)"
read -p "Token: " BOT_TOKEN

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ Token kann nicht leer sein!"
    exit 1
fi

# Frage nach Discord User ID
echo ""
echo "👤 Bitte gib deine Discord User ID ein:"
echo "   (Discord → Einstellungen → Erweitert → Entwicklermodus aktivieren)"
echo "   (Dann Rechtsklick auf dich → ID kopieren)"
read -p "User ID: " USER_ID

if [ -z "$USER_ID" ]; then
    echo "❌ User ID kann nicht leer sein!"
    exit 1
fi

# Optional: Schulportal Credentials in .env
echo ""
echo "💡 Optional: Schulportal Credentials in .env speichern?"
echo "   (Du kannst sie auch später beim /start Command eingeben)"
read -p "Jetzt speichern? (j/n): " save_creds

SCHULPORTAL_USER=""
SCHULPORTAL_PASS=""

if [ "$save_creds" = "j" ]; then
    read -p "Benutzername: " SCHULPORTAL_USER
    read -sp "Passwort: " SCHULPORTAL_PASS
    echo ""
fi

# Frage nach Institution (optional)
echo ""
echo "🏫 Institutions-ID (Standard: 6081, Enter für Standard):"
read -p "Institution: " INSTITUTION
INSTITUTION=${INSTITUTION:-6081}

# Intervalle (optional)
echo ""
echo "⏰ Check-Intervall in Sekunden (Standard: 300 = 5 Min, Enter für Standard):"
read -p "Intervall: " CHECK_INTERVAL
CHECK_INTERVAL=${CHECK_INTERVAL:-300}

# .env Datei erstellen
echo ""
echo "💾 Erstelle .env Datei..."

cat > .env << EOF
# Discord Bot Configuration
DISCORD_BOT_TOKEN=$BOT_TOKEN
DISCORD_USER_ID=$USER_ID

# Schulportal Configuration
SCHULPORTAL_USERNAME=$SCHULPORTAL_USER
SCHULPORTAL_PASSWORD=$SCHULPORTAL_PASS
SCHULPORTAL_INSTITUTION=$INSTITUTION

# Bot Intervals (in seconds)
CHECK_INTERVAL=$CHECK_INTERVAL
EOF

chmod 600 .env  # Nur Owner kann lesen/schreiben

echo "✅ .env erstellt und gesichert"
echo ""

# Stundenplan check
if [ ! -f Stundenplan.txt ]; then
    echo "⚠️  Stundenplan.txt nicht gefunden!"
    echo "   Stelle sicher dass diese Datei existiert bevor du den Bot startest."
    echo ""
fi

# Abschluss
echo "=========================================="
echo "✅ Setup erfolgreich abgeschlossen!"
echo "=========================================="
echo ""
echo "📋 Konfiguration:"
echo "   Discord User ID: $USER_ID"
echo "   Institution: $INSTITUTION"
echo "   Check-Intervall: $CHECK_INTERVAL Sekunden"
if [ -n "$SCHULPORTAL_USER" ]; then
    echo "   Schulportal User: $SCHULPORTAL_USER (in .env gespeichert)"
fi
echo ""
echo "🚀 Starte den Bot mit:"
echo "   python3 discord_bot.py"
echo ""
if [ -z "$SCHULPORTAL_USER" ]; then
    echo "💡 Der Bot wird dich dann nach Schulportal-Login fragen (/start Command)."
else
    echo "💡 Der Bot verwendet die gespeicherten Credentials. (Sende '.' beim /start)"
fi
echo ""
