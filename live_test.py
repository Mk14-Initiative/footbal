import requests
import time
from datetime import datetime

# --- KONFIGURATION ---
VEREIN = "Borussia Dortmund"
LIGA = "bl1" # bl1 = 1. Bundesliga
CHECK_INTERVAL = 10
# ---------------------

def get_match_data():
    """Holt die Spiele des aktuellen Spieltags von OpenLigaDB"""
    url = f"https://api.openligadb.de/getmatchdata/{LIGA}"
    try:
        response = requests.get(url, timeout=10)
        # Nur wenn der Server mit Status 200 (OK) antwortet
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API Fehler: Status {response.status_code}")
            return None
    except Exception as e:
        print(f"Netzwerkfehler: {e}")
        return None

def main():
    last_score = None
    print(f"Überwachung für {VEREIN} gestartet (Strg+C zum Beenden)")

    x = 0

    while x < 2:
        data = get_match_data()

        if data:
            found_today = False
            today = datetime.now().strftime("%Y-%m-%d")

            for match in data:
                home = match['team1']['teamName']
                away = match['team2']['teamName']

                # Prüfen ob unser Verein spielt
                if VEREIN in home or VEREIN in away:
                    match_date = match['matchDateTime'].split('T')[0]

                    if match_date == today:
                        found_today = True
                        results = match['matchResults']

                        # Spielstand ermitteln
                        if results:
                            # Wir nehmen das aktuellste Resultat
                            res = max(results, key=lambda x: x['resultTypeID'])
                            score = f"{res['pointsTeam1']}:{res['pointsTeam2']}"

                            if last_score is None:
                                last_score = score
                                print(f"Spiel läuft: {home} {score} {away}")

                            if score != last_score:
                                print(f"\n!!! TOOOOR !!! Neuer Stand: {score}")
                                # HIER kommt später dein MQTT-Befehl hin
                                last_score = score
                            else:
                                print(f"Live: {score} ({datetime.now().strftime('%H:%M:%S')})", end="\r")
                        else:
                            print(f"Spiel {home} vs {away} fängt heute noch an.", end="\r")
                    else:
                        # Falls das Spiel an einem anderen Tag ist
                        pass

            if not found_today:
                # Kleiner Trick zum Testen: Wenn kein Spiel ist, zeigen wir das zumindest einmal an
                print(f"Heute ({today}) kein Spiel für {VEREIN} gefunden.         ", end="\r")

        #time.sleep(CHECK_INTERVAL)
        x = x +1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgramm beendet.")
