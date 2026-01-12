import requests
from datetime import datetime

# --- KONFIGURATION ---
VEREIN = "Borussia Dortmund"
LIGA = "bl1"
# ---------------------

def check_if_match_today():
    url = f"https://api.openligadb.de/getmatchdata/{LIGA}"
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            matches = response.json()
            found = False

            for match in matches:
                home = match['team1']['teamName']
                away = match['team2']['teamName']

                # Prüfen, ob unser Verein heute spielt
                if VEREIN in home or VEREIN in away:
                    match_date_time = match['matchDateTime'] # Beispiel: "2026-01-12T20:30:00"
                    match_date = match_date_time.split('T')[0]

                    if match_date == today:
                        uhrzeit = match_date_time.split('T')[1][:5] # Extrahiert "20:30"
                        print(f"JA! {home} vs. {away} spielt heute um {uhrzeit} Uhr.")
                        found = True
                        break # Wir haben das Spiel gefunden, Schleife kann stop

            if not found:
                print(f"Nein, heute ({today}) spielt {VEREIN} nicht.")

        else:
            print("Fehler beim Abruf der Daten.")
    except Exception as e:
        print(f"Netzwerkfehler: {e}")

if __name__ == "__main__":
    check_if_match_today()
