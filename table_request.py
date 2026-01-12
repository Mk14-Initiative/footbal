import requests
import time
from datetime import datetime

# EINSTELLUNGEN
LEAGUE = "bl1" # bl1 = 1. Bundesliga
TEAM_NAME = "Borussia Dortmund" # Deinen Verein hier exakt eintragen
INTERVAL = 10 # Prüfintervall in Sekunden

def get_match_data():
    # Dieser Endpunkt liefert die Spiele des aktuellen Spieltags
    url = f"https://api.openligadb.de/getmatchdata/{LEAGUE}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return None

def main():
    last_score = None
    print(f"Überwachung gestartet für: {TEAM_NAME}")

    while True:
        matches = get_match_data()
        today = datetime.now().strftime("%Y-%m-%d") # Format: 2024-05-21

        found_active_match = False

        if matches:
            for match in matches:
                home = match['team1']['teamName']
                away = match['team2']['teamName']
                match_time = match['matchDateTime'] # Kommt als "2024-05-18T15:30:00"

                # Prüfen, ob unser Team spielt UND ob das Spiel HEUTE ist
                if TEAM_NAME in [home, away] and today in match_time:
                    found_active_match = True

                    # Spielstand auslesen
                    results = match['matchResults']
                    if results:
                        current_res = max(results, key=lambda x: x['resultTypeID'])
                        goals_home = current_res['pointsTeam1']
                        goals_away = current_res['pointsTeam2']
                        new_score = f"{goals_home}:{goals_away}"

                        if last_score is None:
                            last_score = new_score
                            print(f"Spiel läuft HEUTE: {home} {new_score} {away}")

                        if new_score != last_score:
                            print(f"!!! TOOOOR !!! Neuer Stand: {new_score}")
                            last_score = new_score
                    else:
                        print(f"Spiel {home} vs {away} beginnt heute um {match_time[11:16]} Uhr.", end="\r")

            if not found_active_match:
                print(f"Kein Spiel für {TEAM_NAME} am heutigen Tag ({today}).", end="\r")

        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
