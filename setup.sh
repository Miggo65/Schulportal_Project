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
    echo "  sudo apt install python3 python3-pip"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION gefunden"
echo ""

# Dependencies installieren
echo "📦 Installiere Python Dependencies..."
pip3 install -r requirements.txt -q

if [ $? -ne 0 ]; then
    echo "❌ Fehler beim Installieren der Dependencies!"
    exit 1
fi

echo "✅ Dependencies installiert"
echo ""

# Playwright Browser installieren
echo "🌐 Installiere Chromium Browser..."
playwright install chromium

if [ $? -ne 0 ]; then
    echo "❌ Fehler beim Installieren von Chromium!"
    echo "Versuche: playwright install-deps chromium"
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

echo ""
echo "📊 Statistik-Intervall in Sekunden (Standard: 3600 = 1 Std, Enter für Standard):"
read -p "Intervall: " STATS_INTERVAL
STATS_INTERVAL=${STATS_INTERVAL:-3600}

# .env Datei erstellen
echo ""
echo "💾 Erstelle .env Datei..."

cat > .env << EOF
# Discord Bot Configuration
DISCORD_BOT_TOKEN=$BOT_TOKEN
DISCORD_USER_ID=$USER_ID

# Schulportal Configuration
SCHULPORTAL_INSTITUTION=$INSTITUTION

# Bot Intervals (in seconds)
CHECK_INTERVAL=$CHECK_INTERVAL
STATS_INTERVAL=$STATS_INTERVAL
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
echo "   Stats-Intervall: $STATS_INTERVAL Sekunden"
echo ""
echo "🚀 Starte den Bot mit:"
echo "   python3 discord_bot.py"
echo ""
echo "💡 Der Bot wird dich dann nach Benutzername und Passwort fragen."
echo ""
