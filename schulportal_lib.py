#!/usr/bin/env python3
"""
Schulportal Hessen Library
Funktionen für Login und Vertretungsplan-Abruf
"""

from playwright.sync_api import Page
from bs4 import BeautifulSoup
import time


def login(page: Page, username: str, password: str, institution_id: str) -> bool:
    """
    Führt den Login im Schulportal durch
    
    Args:
        page: Playwright Page Objekt
        username: Benutzername
        password: Passwort
        institution_id: Institutions-ID (z.B. "6081")
    
    Returns:
        bool: True wenn Login erfolgreich, False sonst
    """
    login_url = f"https://login.schulportal.hessen.de/?i={institution_id}"
    
    print("=" * 60)
    print("LOGIN")
    print("=" * 60)
    print(f"Benutzername: {username}")
    print(f"Login-URL: {login_url}\n")
    
    try:
        # Login-Seite laden
        page.goto(login_url, timeout=30000)
        print("✅ Login-Seite geladen")
        
        # Warte auf das Login-Formular
        page.wait_for_selector("#username2", state="visible", timeout=10000)
        
        # Credentials eingeben
        page.fill("#username2", username)
        page.fill("#inputPassword", password)
        
        print("📝 Login-Daten eingegeben")
        
        # Login-Button klicken
        page.click("button:has-text('Anmelden')")
        
        # Warte auf Navigation
        time.sleep(3)
        
        # Prüfe ob Login erfolgreich
        current_url = page.url
        if "start.schulportal.hessen.de" in current_url:
            print("✅ Login erfolgreich!\n")
            return True
        else:
            print(f"❌ Login fehlgeschlagen!")
            print(f"   Aktuelle URL: {current_url}")
            return False
            
    except Exception as e:
        print(f"❌ Fehler beim Login: {e}")
        return False


def parse_info_table(soup: BeautifulSoup) -> dict:
    """
    Extrahiert die Informationen (Abwesende Lehrer, Hinweise, etc.)
    
    Args:
        soup: BeautifulSoup Objekt
    
    Returns:
        dict: Dictionary mit abwesende_lehrer, hinweis, entfall_klassen
    """
    info = {
        "abwesende_lehrer": "",
        "hinweis": "",
        "entfall_klassen": ""
    }
    
    # Suche die Info-Tabelle mit class="infos"
    info_table = soup.find('table', class_='infos')
    
    if not info_table:
        return info
    
    rows = info_table.find_all('tr')
    current_key = None
    
    for row in rows:
        # Prüfe ob es ein Subheader ist
        if 'subheader' in row.get('class', []):
            header_text = row.get_text(strip=True)
            if "Abwesende Lehrende" in header_text:
                current_key = "abwesende_lehrer"
            elif "Hinweis" in header_text:
                current_key = "hinweis"
            elif "Von Entfall betroffene Klassen" in header_text:
                current_key = "entfall_klassen"
        else:
            # Datenzeile
            if current_key:
                cells = row.find_all('td')
                if cells:
                    text = cells[0].get_text(strip=True)
                    if text and text not in ["Abwesende Lehrende", "Hinweis", "Von Entfall betroffene Klassen"]:
                        info[current_key] = text
    
    return info


def parse_vertretungsplan_table(soup: BeautifulSoup, table_id: str = None) -> dict:
    """
    Extrahiert die Vertretungsplan-Tabelle
    
    Args:
        soup: BeautifulSoup Objekt
        table_id: Optionale Table-ID
    
    Returns:
        dict: Dictionary mit headers, rows, row_count, table_id oder None
    """
    # Finde die Tabelle mit data-toggle="table"
    if table_id:
        table = soup.find('table', id=table_id)
    else:
        table = soup.find('table', {'data-toggle': 'table'})
    
    if not table:
        # Fallback: Suche nach Tabelle mit ID die mit "vtable" beginnt
        all_tables = soup.find_all('table')
        for t in all_tables:
            if t.get('id', '').startswith('vtable'):
                table = t
                break
    
    if not table:
        return None
    
    # Header extrahieren
    headers = []
    thead = table.find('thead')
    if thead:
        for th in thead.find_all('th'):
            # Hole data-field Attribut (das ist der saubere Name)
            field_name = th.get('data-field', '')
            if field_name:
                headers.append(field_name)
            else:
                # Fallback: Text aus th-inner div
                inner = th.find('div', class_='th-inner')
                if inner:
                    headers.append(inner.get_text(strip=True))
                else:
                    headers.append(th.get_text(strip=True))
    
    # Zeilen extrahieren
    rows = []
    tbody = table.find('tbody')
    if tbody:
        for tr in tbody.find_all('tr'):
            row_data = []
            for td in tr.find_all('td'):
                text = td.get_text(strip=True)
                row_data.append(text)
            rows.append(row_data)
    
    return {
        'headers': headers,
        'rows': rows,
        'row_count': len(rows),
        'table_id': table.get('id', 'unknown')
    }


def extract_all_days(soup: BeautifulSoup) -> list:
    """
    Extrahiert alle verfügbaren Tage (auch die versteckten Panels)
    
    Args:
        soup: BeautifulSoup Objekt
    
    Returns:
        list: Liste mit Dictionaries für jeden Tag
    """
    days_data = []
    
    # Finde alle Panels mit id="tag..."
    panels = soup.find_all('div', class_='panel')
    
    for panel in panels:
        panel_id = panel.get('id', '')
        if not panel_id.startswith('tag'):
            continue
        
        # Extrahiere Datum aus dem Panel-Heading
        heading = panel.find('div', class_='panel-heading')
        datum = "Unbekannt"
        badges = []
        
        if heading:
            datum_text = heading.get_text(strip=True)
            # Badges extrahieren (heute, morgen, etc.)
            badge_elems = heading.find_all('span', class_='badge')
            badges = [b.get_text(strip=True) for b in badge_elems]
            
            # Datum extrahieren (z.B. "Montag, den 01.12.2025")
            if ',' in datum_text:
                parts = datum_text.split()
                for part in parts:
                    if '.' in part and len(part) >= 5:  # Format: DD.MM oder DD.MM.YYYY
                        datum = part.replace('den', '').strip()
                        break
        
        # Panel Body
        panel_body = panel.find('div', class_='panel-body')
        if not panel_body:
            continue
        
        # Informationen extrahieren
        info = parse_info_table(BeautifulSoup(str(panel_body), 'html.parser'))
        
        # Vertretungsplan-Tabelle extrahieren
        table_id = f"vtable{panel_id.replace('tag', '')}"
        table_data = parse_vertretungsplan_table(BeautifulSoup(str(panel_body), 'html.parser'), table_id)
        
        # Letzte Aktualisierung
        update_elem = panel_body.find('i', string=lambda t: t and 'Letzte Aktualisierung' in t)
        update_time = update_elem.get_text(strip=True) if update_elem else "Unbekannt"
        
        days_data.append({
            'datum': datum,
            'badges': badges,
            'panel_id': panel_id,
            'informationen': info,
            'vertretungen': table_data,
            'letzte_aktualisierung': update_time
        })
    
    return days_data


def get_vertretungsplan(page: Page) -> dict:
    """
    Lädt den Vertretungsplan und extrahiert alle Daten
    
    Args:
        page: Playwright Page Objekt (muss bereits eingeloggt sein)
    
    Returns:
        dict: Dictionary mit allen Vertretungsplan-Daten oder None bei Fehler
    """
    vp_url = "https://start.schulportal.hessen.de/vertretungsplan.php"
    
    print("=" * 60)
    print("VERTRETUNGSPLAN ABRUFEN")
    print("=" * 60)
    print(f"URL: {vp_url}\n")
    
    try:
        # Vertretungsplan-Seite laden
        page.goto(vp_url, timeout=30000)
        print(f"✅ Vertretungsplan-Seite geladen")
        
        # Warte bis die Tabelle geladen ist
        page.wait_for_selector('table[data-toggle="table"]', timeout=10000)
        print("✅ Tabelle gefunden")
        
        # Warte kurz damit alles vollständig geladen ist
        time.sleep(2)
        
        # Hole HTML-Content
        html_content = page.content()
        
        # HTML parsen
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extrahiere alle Tage
        print("\n📅 Extrahiere Daten für alle Tage...")
        all_days = extract_all_days(soup)
        
        print(f"✅ {len(all_days)} Tag(e) gefunden:")
        for day in all_days:
            badges_str = ', '.join(day['badges']) if day['badges'] else ''
            vp_count = day['vertretungen']['row_count'] if day['vertretungen'] else 0
            print(f"   - {day['datum']} ({badges_str}): {vp_count} Vertretung(en)")
        
        # Gesamtresultat
        from datetime import datetime
        result = {
            'zeitstempel': datetime.now().isoformat(),
            'tage': all_days,
            'anzahl_tage': len(all_days)
        }
        
        return result
        
    except Exception as e:
        print(f"❌ Fehler beim Abrufen: {e}")
        import traceback
        traceback.print_exc()
        return None
