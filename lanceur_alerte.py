#!/usr/bin/env python3

import json
import subprocess
import time
import os

def notify(title, message):
    subprocess.run(['notify-send', title, message])

def tail_f(file_path):
    with open(file_path, 'r') as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            yield line

def monitor_suricata(eve_json_path="/var/log/suricata/eve.json"):
    print(f"Surveillance de {eve_json_path} en cours...")

    # Dictionnaire pour éviter le spam (alerte -> timestamp dernier envoi)
    alert_cache = {}

    # Délais minimal entre notifications identiques (en secondes)
    cooldown = 30

    for line in tail_f(eve_json_path):
        try:
            event = json.loads(line)
            if event.get("event_type") == "alert":
                signature = event["alert"].get("signature", "Alerte inconnue")
                src_ip = event.get("src_ip", "inconnu")
                dest_ip = event.get("dest_ip", "inconnu")
                msg = f"{signature}\nDe: {src_ip} -> {dest_ip}"

                now = time.time()

                # Si on n’a jamais vu cette alerte ou si cooldown dépassé
                if signature not in alert_cache or now - alert_cache[signature] > cooldown:
                    notify("🚨 Suricata Alert", msg)
                    print(f"[ALERTE] {msg}")
                    alert_cache[signature] = now

        except json.JSONDecodeError:
            continue

if __name__ == "__main__":
    monitor_suricata("/var/log/suricata/eve.json")
