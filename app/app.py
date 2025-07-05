from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from collections import defaultdict
from datetime import datetime, timezone
import locale

app = Flask(__name__)

# === BASE DIR ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# === CONFIG ===
MINI_LOG_PATH = os.path.join(BASE_DIR, "mini_eve.json")
USER_RULES_PATH = os.path.join(BASE_DIR, "user_rules.txt")
DEFAULT_LOGS_PER_CATEGORY = 20
CACHE_REFRESH_INTERVAL = 30  # secondes

# === LOCALE ===
try:
    locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
except locale.Error:
    locale.setlocale(locale.LC_TIME, "C")

# === CACHE ===
logs_cache = {
    "all_logs": [],
    "last_update": 0,
    "dates": []
}

# === UTILS ===
def time_since(dt):
    now = datetime.now(timezone.utc)
    diff = now - dt
    seconds = diff.total_seconds()
    if seconds < 60:
        return "il y a quelques secondes"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"il y a {minutes} min"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"il y a {hours} h"
    else:
        days = int(seconds // 86400)
        return f"il y a {days} j"

def load_mini_logs():
    if not os.path.exists(MINI_LOG_PATH):
        return [], []

    with open(MINI_LOG_PATH, "r") as f:
        data = json.load(f)

    dates = sorted(set(log["date_only"] for log in data if log["date_only"] != "unknown"))
    return data, dates

# === ROUTES ===
@app.route("/")
def index():
    date_filter = request.args.get("date", None)
    current_time = datetime.now().timestamp()

    if current_time - logs_cache["last_update"] > CACHE_REFRESH_INTERVAL:
        all_logs, dates = load_mini_logs()
        logs_cache["all_logs"] = all_logs
        logs_cache["dates"] = dates
        logs_cache["last_update"] = current_time
    else:
        all_logs = logs_cache["all_logs"]
        dates = logs_cache["dates"]

    filtered_logs = all_logs
    if date_filter:
        filtered_logs = [log for log in all_logs if log["date_only"] == date_filter]

    logs_by_category = defaultdict(list)
    for log in filtered_logs:
        logs_by_category[log["signature"]].append(log)

    logs_preview = {}
    for sig, logs in logs_by_category.items():
        logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        for log in logs:
            try:
                dt = datetime.fromisoformat(log["timestamp"].replace("Z", "+00:00"))
                log["relative_time"] = time_since(dt)
            except:
                log["relative_time"] = "Inconnu"
        logs_preview[sig] = logs[:DEFAULT_LOGS_PER_CATEGORY]

    sorted_logs = sorted(logs_preview.items(), key=lambda x: x[0])

    return render_template("index.html", logs=sorted_logs, dates=dates, selected_date=date_filter)

@app.route("/load_all")
def load_all():
    signature = request.args.get("signature")
    date_filter = request.args.get("date")

    all_logs = logs_cache["all_logs"]
    if date_filter:
        all_logs = [log for log in all_logs if log["date_only"] == date_filter]

    logs = [log for log in all_logs if log["signature"] == signature]
    logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

    for log in logs:
        try:
            dt = datetime.fromisoformat(log["timestamp"].replace("Z", "+00:00"))
            log["relative_time"] = time_since(dt)
        except:
            log["relative_time"] = "Inconnu"

    return jsonify(logs)

@app.route("/rules", methods=["GET", "POST"])
def rules():
    LOCAL_RULES_PATH = "/etc/suricata/rules/local.rules"

    if request.method == "POST":
        protocol = request.form.get("protocol")
        port = request.form.get("port", "")
        message = request.form.get("message", "")

        rule = f'alert {protocol} any any -> any {port if port else "any"} (msg:"{message}"; sid:{int(datetime.now().timestamp()) % 100000}; rev:1;)'

        # Créer le fichier si nécessaire
        if not os.path.exists(USER_RULES_PATH):
            with open(USER_RULES_PATH, "w") as f:
                pass

        try:
            with open(USER_RULES_PATH, "a") as f:
                f.write("\n" + rule.strip())
        except Exception as e:
            return f"Erreur lors de l'ajout de la règle: {e}"

        return redirect(url_for("rules"))

    # Lire user_rules.txt
    if os.path.exists(USER_RULES_PATH):
        with open(USER_RULES_PATH, "r") as f:
            user_rules = f.read()
    else:
        user_rules = "Aucune règle ajoutée via l'interface."

    # Lire local.rules
    if os.path.exists(LOCAL_RULES_PATH):
        try:
            with open(LOCAL_RULES_PATH, "r") as f:
                local_rules = f.read()
        except Exception as e:
            local_rules = f"Erreur de lecture du fichier local.rules : {e}"
    else:
        local_rules = "Le fichier local.rules n'existe pas."

    return render_template("rules.html", rules=user_rules, local_rules=local_rules)

# === MAIN ===
if __name__ == "__main__":
    # Créer les fichiers si n'existent pas
    if not os.path.exists(USER_RULES_PATH):
        with open(USER_RULES_PATH, "w") as f:
            pass
    if not os.path.exists(MINI_LOG_PATH):
        with open(MINI_LOG_PATH, "w") as f:
            f.write("[]")

    app.run(host="0.0.0.0", port=5000)
