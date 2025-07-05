import json
import os
from dateutil import parser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EVE_LOG_PATH = "/var/log/suricata/eve.json"  # ← tu laisses ce chemin si c’est là que Suricata écrit
MINI_LOG_PATH = os.path.join(BASE_DIR, "mini_eve.json")
TAIL_LINES = 5000

def tail(filename, n=5000):
    with open(filename, 'rb') as f:
        f.seek(0, 2)
        file_size = f.tell()
        block_size = 1024
        data = b''
        while file_size > 0 and data.count(b'\n') <= n:
            delta = min(block_size, file_size)
            f.seek(file_size - delta)
            data = f.read(delta) + data
            file_size -= delta
        lines = data.splitlines()[-n:]
    return [line.decode('utf-8', errors='ignore') for line in lines]

def prepare_mini_log():
    mini_logs = []

    if not os.path.exists(EVE_LOG_PATH):
        print("Fichier eve.json non trouvé.")
        return

    for line in tail(EVE_LOG_PATH, n=TAIL_LINES):
        try:
            data = json.loads(line)
            if data.get("event_type") == "alert":
                raw_timestamp = data.get("timestamp", "")
                try:
                    dt = parser.isoparse(raw_timestamp)
                    formatted_time = dt.strftime("%d %B %Y, %H:%M:%S")
                    date_only = dt.strftime("%Y-%m-%d")
                except:
                    formatted_time = raw_timestamp
                    date_only = "unknown"

                mini_logs.append({
                    "signature": data["alert"].get("signature", "Inconnue"),
                    "src_ip": data.get("src_ip", ""),
                    "dest_ip": data.get("dest_ip", ""),
                    "timestamp": raw_timestamp,
                    "formatted_time": formatted_time,
                    "date_only": date_only
                })
        except json.JSONDecodeError:
            continue

    with open(MINI_LOG_PATH, "w") as f:
        json.dump(mini_logs, f, indent=2)

    print(f"✅ Mini log généré : {MINI_LOG_PATH} ({len(mini_logs)} logs)")

if __name__ == "__main__":
    prepare_mini_log()
