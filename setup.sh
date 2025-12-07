#!/bin/bash

# Quick Setup Script für Discord Bot

echo "=========================================="
echo "Schulportal Discord Bot - Quick Setup"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 nicht gefunden!"
    echo "Bitte installiere Python 3.8 oder höher."
    exit 1
fi

echo "✅ Python gefunden: $(python3 --version)"
echo ""

# Dependencies installieren
echo "📦 Installiere Dependencies..."
pip3 install -r requirements.txt

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
    exit 1
fi

echo "✅ Chromium installiert"
echo ""

# .env erstellen falls nicht vorhanden
if [ ! -f .env ]; then
    echo "📝 Erstelle .env Datei..."
    cp .env.example .env
    echo "✅ .env erstellt"
    echo ""
    echo "⚠️  WICHTIG: Bearbeite jetzt die .env Datei!"
    echo "   Füge dein Discord Bot Token ein:"
    echo "   nano .env"
    echo ""
else
    echo "✅ .env existiert bereits"
    echo ""
fi

# Stundenplan check
if [ ! -f Stundenplan.txt ]; then
    echo "⚠️  Stundenplan.txt nicht gefunden!"
    echo "   Erstelle diese Datei mit deinem Stundenplan."
    echo ""
fi

echo "=========================================="
echo "✅ Setup abgeschlossen!"
echo "=========================================="
echo ""
echo "Nächste Schritte:"
echo "1. Bearbeite .env mit deinem Bot Token:"
echo "   nano .env"
echo ""
echo "2. Stelle sicher dass Stundenplan.txt existiert"
echo ""
echo "3. Starte den Bot:"
echo "   python3 discord_bot.py"
echo ""
echo "4. Schreibe /start in Discord DM zum Bot"
echo ""
