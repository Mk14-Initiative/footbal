import requests
import time
import paho.mqtt.client as mqtt

# --- KONFIGURATION ---
VEREIN = "Eintracht Frankfurt"
MQTT_BROKER = "localhost" # IP deines Pi
MQTT_TOPIC = "fussball/event"
CHECK_INTERVAL = 5 # Sekunden während des Spiels
# ---------------------

client = mqtt.Client()

def get_today_match_id():
    """Findet die Match-ID für den heutigen Tag"""
    # Übersicht der heutigen Spiele (Beispiel Bundesliga)
    url = "https://www.sportschau.de/live-und-ergebnisse/fussball/deutschland-bundesliga/alle-spiele-heute-json/"
    try:
        data = requests.get(url).json()
        for match in data.get('matches', []):
            home = match['homeTeam']['name']
            away = match['awayTeam']['name']
            if VEREIN in [home, away]:
                return match['matchID']
    except Exception as e:
        print(f"Fehler bei Match-Suche: {e}")
    return None

def monitor_game(match_id):
    """Überwacht das spezifische Spiel auf Tore"""
    url = f"https://www.sportschau.de/live-und-ergebnisse/fussball/deutschland-bundesliga/{match_id}/liveticker-json/"
    last_score = None

    print(f"Überwachung für Match {match_id} gestartet...")

    while True:
        try:
            data = requests.get(url).json()
            score_home = data['score']['home']
            score_away = data['score']['away']
            current_score = f"{score_home}:{score_away}"

            if last_score is None:
                last_score = current_score
                print(f"Start-Spielstand: {current_score}")

            if current_score != last_score:
                print(f"TOOOOR! Neuer Stand: {current_score}")
                client.connect(MQTT_BROKER)
                client.publish(MQTT_TOPIC, f"TOR_{current_score}")
                client.disconnect()
                last_score = current_score

            # Check ob Spiel vorbei
            if data.get('matchFinished'):
                print("Spiel beendet.")
                break

        except Exception as e:
            print(f"Fehler im Live-Ticker: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    # 1. Match suchen
    mid = get_today_match_id()
    if mid:
        monitor_game(mid)
    else:
        print(f"Heute kein Spiel für {VEREIN} gefunden.")
