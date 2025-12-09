#!/usr/bin/env python3
"""
Discord Bot für Schulportal Vertretungsplan
Automatische Benachrichtigungen bei neuen Ausfällen alle 5 Minuten
"""

import discord
from discord.ext import commands, tasks
import os
import asyncio
import json
from datetime import datetime
from dotenv import load_dotenv
from playwright.async_api import async_playwright
import logging

# Importiere unsere Module
from schulportal_lib import login, get_vertretungsplan
from stundenplan_checker import StundenplanChecker

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('VertretungsplanBot')

# Lade .env Datei
load_dotenv()

# Bot Setup - Nur default intents
intents = discord.Intents.default()
intents.message_content = True  # Für Commands
bot = commands.Bot(command_prefix='/', intents=intents)

# Globale Variablen
user_credentials = {}
scan_stats = {
    'total_scans': 0,
    'successful_scans': 0,
    'failed_scans': 0,
    'last_scan': None,
    'new_ausfaelle_found': 0
}
is_monitoring = False
target_user_id = int(os.getenv('DISCORD_USER_ID'))


def load_stats():
    """Lade Statistiken aus JSON"""
    global scan_stats
    try:
        if os.path.exists('bot_stats.json'):
            with open('bot_stats.json', 'r') as f:
                scan_stats = json.load(f)
                logger.info("Statistiken geladen")
    except Exception as e:
        logger.error(f"Fehler beim Laden der Statistiken: {e}")


def save_stats():
    """Speichere Statistiken in JSON"""
    try:
        with open('bot_stats.json', 'w') as f:
            json.dump(scan_stats, f, indent=2)
    except Exception as e:
        logger.error(f"Fehler beim Speichern der Statistiken: {e}")


async def check_vertretungsplan():
    """Prüfe Vertretungsplan und sende Benachrichtigungen"""
    global scan_stats, is_monitoring
    
    if not user_credentials:
        logger.warning("Keine Credentials gesetzt. Überspringe Scan.")
        return
    
    try:
        scan_stats['total_scans'] += 1
        logger.info(f"Starte Scan #{scan_stats['total_scans']}")
        
        # Playwright Browser starten
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # Login (wir müssen die synchronen Funktionen anpassen)
                from concurrent.futures import ThreadPoolExecutor
                
                def sync_check():
                    from playwright.sync_api import sync_playwright
                    with sync_playwright() as p_sync:
                        browser_sync = p_sync.chromium.launch(headless=True)
                        page_sync = browser_sync.new_page()
                        
                        # Login
                        if not login(page_sync, 
                                   user_credentials['username'],
                                   user_credentials['password'],
                                   user_credentials.get('institution', '6081')):
                            logger.error("Login fehlgeschlagen")
                            return None
                        
                        # Vertretungsplan abrufen
                        vp_data = get_vertretungsplan(page_sync)
                        browser_sync.close()
                        return vp_data
                
                # Führe in Thread-Pool aus
                with ThreadPoolExecutor() as executor:
                    vp_data = await asyncio.get_event_loop().run_in_executor(
                        executor, sync_check
                    )
                
                if not vp_data:
                    scan_stats['failed_scans'] += 1
                    save_stats()
                    logger.error("Fehler beim Abrufen des Vertretungsplans")
                    return
                
                # Stundenplan-Check
                checker = StundenplanChecker()
                ausfaelle = checker.check_vertretungsplan(vp_data)
                
                # Neue Ausfälle finden
                neue_ausfaelle = [a for a in ausfaelle if a['neu']]
                
                if neue_ausfaelle:
                    scan_stats['new_ausfaelle_found'] += len(neue_ausfaelle)
                    logger.info(f"🚨 {len(neue_ausfaelle)} neue Ausfälle gefunden!")
                    
                    # Sende Discord-Nachricht
                    user = await bot.fetch_user(target_user_id)
                    if user:
                        for ausfall in neue_ausfaelle:
                            embed = discord.Embed(
                                title="🚨 NEUER AUSFALL!",
                                color=discord.Color.red(),
                                timestamp=datetime.now()
                            )
                            embed.add_field(name="📅 Datum", 
                                          value=f"{ausfall['wochentag']}, {ausfall['datum']}", 
                                          inline=False)
                            embed.add_field(name="⏰ Stunde", 
                                          value=str(ausfall['stunde']), 
                                          inline=True)
                            embed.add_field(name="👨‍🏫 Lehrer", 
                                          value=ausfall['lehrer'], 
                                          inline=True)
                            embed.set_footer(text=f"Scan #{scan_stats['total_scans']}")
                            
                            await user.send(embed=embed)
                            await asyncio.sleep(0.5)  # Rate limiting
                
                scan_stats['successful_scans'] += 1
                scan_stats['last_scan'] = datetime.now().isoformat()
                save_stats()
                logger.info(f"✅ Scan erfolgreich. Neue Ausfälle: {len(neue_ausfaelle)}")
                
            finally:
                await browser.close()
                
    except Exception as e:
        scan_stats['failed_scans'] += 1
        save_stats()
        logger.error(f"❌ Fehler beim Scan: {e}", exc_info=True)


@tasks.loop(seconds=300)  # 5 Minuten
async def monitoring_loop():
    """Haupt-Monitoring-Loop"""
    if is_monitoring:
        await check_vertretungsplan()


@bot.event
async def on_ready():
    """Bot ist bereit"""
    logger.info(f'Bot eingeloggt als {bot.user}')
    load_stats()
    
    # Sende "Bereit"-Nachricht
    user = await bot.fetch_user(target_user_id)
    if user:
        embed = discord.Embed(
            title="✅ Vertretungsplan Bot ist bereit!",
            description="Verwende `/start` um das Monitoring zu starten.",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.add_field(name="Commands", 
                       value="`/start` - Monitoring starten\n`/stop` - Monitoring stoppen\n`/scanstatus` - Status anzeigen", 
                       inline=False)
        await user.send(embed=embed)
        logger.info("✅ Bereit-Nachricht gesendet")


@bot.command(name='start')
async def start_monitoring(ctx):
    """Starte Monitoring - fordert Credentials an"""
    global is_monitoring, user_credentials
    
    if ctx.author.id != target_user_id:
        await ctx.send("❌ Du bist nicht autorisiert, diesen Bot zu verwenden.")
        return
    
    if is_monitoring:
        await ctx.send("⚠️ Monitoring läuft bereits!")
        return
    
    # Frage nach Credentials
    await ctx.send("📝 Bitte gib deinen **Benutzernamen** für das Schulportal ein:\n(Sende `.` für Standard aus .env)")
    
    def check(m):
        return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)
    
    try:
        # Username
        username_msg = await bot.wait_for('message', check=check, timeout=60.0)
        username = username_msg.content.strip()
        if username == ".":
            username = os.getenv('SCHULPORTAL_USERNAME', '')
            if not username:
                await ctx.send("❌ Kein Standard-Benutzername in .env gefunden!")
                return
            await ctx.send(f"✅ Verwende Standard-Benutzername aus .env")
        
        # Password mit Spoiler-Tags
        await ctx.send("🔒 Bitte gib dein **Passwort** ein:\n⚠️ **Wichtig:** Schreibe es so: `||deinPasswort||` (mit ||...||)\nDies markiert es als Spoiler und schützt es vor fremden Blicken.\n(Sende `.` für Standard aus .env)")
        password_msg = await bot.wait_for('message', check=check, timeout=60.0)
        password = password_msg.content.strip()
        
        if password == ".":
            password = os.getenv('SCHULPORTAL_PASSWORD', '')
            if not password:
                await ctx.send("❌ Kein Standard-Passwort in .env gefunden!")
                return
            await ctx.send(f"✅ Verwende Standard-Passwort aus .env")
        else:
            # Entferne Spoiler-Tags falls vorhanden
            password = password.replace('||', '').strip()
        
        # Lösche Passwort-Nachricht
        try:
            await password_msg.delete()
        except:
            pass
        
        # Optional: Institution
        await ctx.send("🏫 Institutions-ID (Standard: 6081, sende `.` für Standard):")
        institution_msg = await bot.wait_for('message', check=check, timeout=30.0)
        institution_input = institution_msg.content.strip()
        
        if institution_input == "." or institution_input == "":
            institution = os.getenv('SCHULPORTAL_INSTITUTION', '6081')
        else:
            institution = institution_input
        
        # Speichere Credentials
        user_credentials = {
            'username': username,
            'password': password,
            'institution': institution
        }
        
        # Starte Monitoring
        is_monitoring = True
        monitoring_loop.start()
        
        embed = discord.Embed(
            title="✅ Monitoring gestartet!",
            description=f"Prüfe alle 5 Minuten auf neue Ausfälle.",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.add_field(name="Benutzername", value=username, inline=True)
        embed.add_field(name="Institution", value=institution, inline=True)
        await ctx.send(embed=embed)
        
        logger.info(f"✅ Monitoring gestartet für Benutzer {username}")
        
        # Führe ersten Check durch
        await check_vertretungsplan()
        
    except asyncio.TimeoutError:
        await ctx.send("❌ Timeout - Vorgang abgebrochen.")
    except Exception as e:
        await ctx.send(f"❌ Fehler: {e}")
        logger.error(f"Fehler beim Start: {e}", exc_info=True)


@bot.command(name='stop')
async def stop_monitoring(ctx):
    """Stoppe Monitoring"""
    global is_monitoring
    
    if ctx.author.id != target_user_id:
        await ctx.send("❌ Du bist nicht autorisiert.")
        return
    
    if not is_monitoring:
        await ctx.send("⚠️ Monitoring läuft nicht.")
        return
    
    is_monitoring = False
    monitoring_loop.cancel()
    
    await ctx.send("⏹️ Monitoring gestoppt.")
    logger.info("⏹️ Monitoring gestoppt")


@bot.command(name='scanstatus')
async def show_status(ctx):
    """Zeige Scan-Status und Statistiken"""
    if ctx.author.id != target_user_id:
        await ctx.send("❌ Du bist nicht autorisiert.")
        return
    
    status = "🟢 Aktiv" if is_monitoring else "🔴 Inaktiv"
    
    embed = discord.Embed(
        title="📊 Scan-Status",
        color=discord.Color.green() if is_monitoring else discord.Color.red(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Status", value=status, inline=False)
    embed.add_field(name="Gesamt Scans", value=str(scan_stats['total_scans']), inline=True)
    embed.add_field(name="Erfolgreich", value=str(scan_stats['successful_scans']), inline=True)
    embed.add_field(name="Fehlgeschlagen", value=str(scan_stats['failed_scans']), inline=True)
    embed.add_field(name="Neue Ausfälle gefunden", value=str(scan_stats['new_ausfaelle_found']), inline=True)
    
    if scan_stats['last_scan']:
        last_scan = datetime.fromisoformat(scan_stats['last_scan'])
        embed.add_field(name="Letzter Scan", 
                       value=last_scan.strftime('%d.%m.%Y %H:%M:%S'), 
                       inline=False)
    
    await ctx.send(embed=embed)


def main():
    """Hauptfunktion"""
    token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not token:
        logger.error("❌ DISCORD_BOT_TOKEN nicht in .env gefunden!")
        print("\n❌ Fehler: DISCORD_BOT_TOKEN nicht gefunden!")
        print("Erstelle eine .env Datei mit deinem Bot Token:")
        print("DISCORD_BOT_TOKEN=dein_token_hier")
        return
    
    logger.info("🚀 Starte Discord Bot...")
    bot.run(token)


if __name__ == "__main__":
    main()
