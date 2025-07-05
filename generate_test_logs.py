#!/usr/bin/env python3
"""
Script pour générer des logs de test Suricata
Utile si vous n'avez pas encore de vrais logs Suricata
"""

import json
import os
from datetime import datetime, timedelta

def generate_test_logs():
    """Génère des logs de test au format Suricata EVE JSON"""
    
    test_logs = []
    signatures = [
        "ET SCAN Suspicious inbound to mySQL port 3306",
        "ET DROP Spamhaus SBL Listed Traffic",
        "ET POLICY SSH brute force attack",
        "ET SCAN Potential SSH Scan",
        "ET MALWARE Win32/Trojan Generic",
        "ET INFO Executable Download",
        "ET SCAN Port Scan",
        "ET POLICY External IP Lookup",
        "ET TROJAN Possible Backdoor",
        "ET WEB_SPECIFIC_APPS SQL Injection Attack"
    ]
    
    src_ips = [
        "192.168.1.10", "192.168.1.15", "10.0.0.5", 
        "172.16.0.10", "203.0.113.1", "198.51.100.1"
    ]
    
    dest_ips = [
        "192.168.1.100", "192.168.1.200", "10.0.0.1",
        "172.16.0.1"
    ]
    
    # Générer 100 logs de test répartis sur les 7 derniers jours
    base_time = datetime.now()
    
    for i in range(100):
        # Varier les timestamps sur 7 jours
        days_ago = i % 7
        hours_ago = (i * 2) % 24
        timestamp = base_time - timedelta(days=days_ago, hours=hours_ago)
        
        log = {
            "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "event_type": "alert",
            "src_ip": src_ips[i % len(src_ips)],
            "src_port": 1024 + (i * 17) % 60000,
            "dest_ip": dest_ips[i % len(dest_ips)],
            "dest_port": [22, 80, 443, 3306, 53][i % 5],
            "proto": "TCP",
            "alert": {
                "signature": signatures[i % len(signatures)],
                "signature_id": 2000000 + i,
                "severity": [1, 2, 3][i % 3],
                "category": "Attempted Information Leak"
            },
            "flow": {
                "pkts_toserver": 1 + i % 10,
                "pkts_toclient": 1 + i % 5,
                "bytes_toserver": 60 + (i * 23) % 500,
                "bytes_toclient": 40 + (i * 31) % 300
            }
        }
        test_logs.append(json.dumps(log))
    
    return test_logs

def save_test_logs(logs, filename="test_eve.json"):
    """Sauvegarde les logs dans un fichier"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for log in logs:
                f.write(log + "\n")
        
        print(f"✅ Fichier de test créé : {filename}")
        print(f"📊 Nombre de logs générés : {len(logs)}")
        return True
    
    except Exception as e:
        print(f"❌ Erreur lors de la création du fichier : {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Génération de logs de test Suricata...")
    
    # Générer les logs
    test_logs = generate_test_logs()
    
    # Sauvegarder dans le fichier
    if save_test_logs(test_logs):
        print("\n📝 Instructions :")
        print("1. Modifiez temporairement prepare_mini_log.py :")
        print("   EVE_LOG_PATH = 'test_eve.json'")
        print("2. Exécutez : python prepare_mini_log.py")
        print("3. Lancez l'interface : python app.py")
        print("4. Ouvrez http://localhost:5000")
        
        # Vérifier si on est dans le bon répertoire
        if os.path.exists("app"):
            print("\n💡 Conseil : Placez test_eve.json dans le dossier app/ pour plus de simplicité")

if __name__ == "__main__":
    main()
