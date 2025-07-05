# 👨‍💻 Guide du Développeur - Lanceur d'Alerte Suricata

Guide pour comprendre, modifier et étendre le projet.

## 🏗️ Architecture du Code

### Structure Générale

```
lanceur_alerte/
├── lanceur_alerte.py          # Moniteur temps réel
├── app/                       # Application web
│   ├── app.py                 # Serveur Flask principal
│   ├── prepare_mini_log.py    # Traitement des logs
│   ├── merge_rules.py         # Gestion des règles
│   └── templates/             # Interfaces HTML
├── generate_test_logs_correct.py  # Générateur de données test
└── *.md                       # Documentation
```

### Flux de Données

```
Logs Suricata (/var/log/suricata/eve.json)
           ↓
    prepare_mini_log.py (traitement)
           ↓
    mini_eve.json (cache optimisé)
           ↓
    app.py (interface web)
           ↓
    Navigateur (visualisation)
```

## 🔧 Modules Principaux

### 1. lanceur_alerte.py

**Rôle :** Surveillance en temps réel et notifications

**Fonctionnalités clés :**
- `tail_f()` : Lecture continue du fichier de logs
- `monitor_suricata()` : Boucle principale de surveillance
- `notify()` : Envoi de notifications système
- Cache anti-spam avec cooldown configurable

**Points d'extension :**
```python
# Ajouter d'autres types de notifications
def notify_email(title, message):
    # Implémentation email
    pass

def notify_webhook(title, message):
    # Implémentation webhook/Slack
    pass
```

### 2. app/app.py

**Rôle :** Interface web Flask

**Routes principales :**
- `/` : Dashboard principal avec filtrage
- `/load_all` : Chargement AJAX des détails
- `/rules` : Gestion des règles

**Cache système :**
```python
logs_cache = {
    "all_logs": [],      # Logs en mémoire
    "last_update": 0,    # Timestamp MAJ
    "dates": []          # Dates disponibles
}
```

**Points d'extension :**
- Ajouter une API REST
- Intégrer une base de données
- Ajouter l'authentification
- Métriques et statistiques avancées

### 3. app/prepare_mini_log.py

**Rôle :** Optimisation des logs Suricata

**Transformations :**
- Filtrage (alertes uniquement)
- Formatage des timestamps
- Extraction des champs essentiels
- Génération du cache JSON

**Optimisations possibles :**
- Indexation par date/IP/signature
- Compression des données
- Base de données au lieu de JSON

## 📊 Format des Données

### Log Suricata Original
```json
{
  "timestamp": "2025-07-05T10:30:00.123456Z",
  "event_type": "alert",
  "src_ip": "192.168.1.10",
  "src_port": 12345,
  "dest_ip": "192.168.1.100", 
  "dest_port": 80,
  "alert": {
    "signature": "ET SCAN Port Scan",
    "signature_id": 2000001,
    "severity": 3
  }
}
```

### Log Optimisé (mini_eve.json)
```json
{
  "signature": "ET SCAN Port Scan",
  "src_ip": "192.168.1.10",
  "dest_ip": "192.168.1.100",
  "timestamp": "2025-07-05T10:30:00.123456Z",
  "formatted_time": "5 juillet 2025, 10:30:00",
  "date_only": "2025-07-05"
}
```

## 🎨 Interface Utilisateur

### Technologies Utilisées
- **Backend :** Flask (Python)
- **Frontend :** HTML/CSS/JavaScript vanilla
- **Calendrier :** Flatpickr
- **Style :** CSS personnalisé (mode sombre)

### Structure des Templates

**index.html :**
- Filtrage par date
- Affichage par catégories
- Chargement AJAX pour les détails
- Interface responsive

**rules.html :**
- Formulaire de création de règles
- Visualisation des règles existantes
- Interface de gestion

### Personnalisation CSS

Variables de couleurs principales :
```css
:root {
  --primary-color: #007bff;
  --secondary-color: #343a40;
  --background-color: #f0f2f5;
  --card-background: #ffffff;
  --text-color: #333333;
}
```

## 🔌 Extensions Suggérées

### 1. API REST

Ajouter des endpoints pour intégration externe :

```python
@app.route("/api/alerts")
def api_alerts():
    return jsonify({"alerts": filtered_logs})

@app.route("/api/stats")
def api_stats():
    return jsonify({"total": count, "by_type": stats})
```

### 2. Base de Données

Remplacer JSON par SQLite/PostgreSQL :

```sql
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    signature VARCHAR(255),
    src_ip INET,
    dest_ip INET,
    timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 3. Authentification

Ajouter Flask-Login :

```python
from flask_login import login_required

@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html")
```

### 4. Monitoring Avancé

Intégrer Prometheus/Grafana :

```python
from prometheus_client import Counter, Histogram

alert_counter = Counter('suricata_alerts_total', 'Total alerts')
response_time = Histogram('flask_request_duration_seconds', 'Request duration')
```

## 🧪 Tests et Debugging

### Tests Unitaires

Créer `test_app.py` :

```python
import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
```

### Debugging Flask

Mode développement :
```python
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
```

### Profiling Performance

```python
from flask import g
import time

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - g.start_time
    print(f"Request took {duration:.2f}s")
    return response
```

## 📈 Optimisations Performance

### 1. Cache Redis

```python
import redis
r = redis.Redis()

def get_cached_logs():
    cached = r.get("logs_cache")
    if cached:
        return json.loads(cached)
    return None
```

### 2. Pagination

```python
@app.route("/api/alerts")
def api_alerts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    start = (page - 1) * per_page
    end = start + per_page
    
    return jsonify({
        "alerts": logs[start:end],
        "page": page,
        "total": len(logs)
    })
```

### 3. Indexation

```python
from collections import defaultdict

# Index par IP source
ip_index = defaultdict(list)
for log in logs:
    ip_index[log["src_ip"]].append(log)
```

## 🚀 Déploiement Production

### 1. WSGI Server (Gunicorn)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 2. Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. Systemd Service

```ini
[Unit]
Description=Lanceur Alerte Web
After=network.target

[Service]
Type=exec
User=www-data
WorkingDirectory=/path/to/app
ExecStart=/usr/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

## 🔒 Sécurité

### Bonnes Pratiques

1. **Variables d'environnement :**
```python
import os
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
```

2. **Validation des entrées :**
```python
from flask_wtf import FlaskForm
from wtforms import StringField, validators

class RuleForm(FlaskForm):
    protocol = StringField('Protocol', [validators.Length(min=3, max=5)])
```

3. **HTTPS uniquement :**
```python
@app.before_request
def force_https():
    if not request.is_secure and app.env != 'development':
        return redirect(request.url.replace('http://', 'https://'))
```

## 🤝 Contribution

### Workflow Git

1. Fork du repository
2. Créer une branche feature : `git checkout -b feature/nouvelle-fonctionnalite`
3. Commit des changes : `git commit -am 'Ajout nouvelle fonctionnalité'`
4. Push vers la branche : `git push origin feature/nouvelle-fonctionnalite`
5. Créer une Pull Request

### Standards de Code

- **Python :** PEP 8
- **JavaScript :** ES6+
- **CSS :** BEM methodology
- **Documentation :** Docstrings Google Style

### Tests Requis

Avant chaque PR :
```bash
# Tests unitaires
python -m pytest tests/

# Linting
flake8 app/
black app/

# Sécurité
bandit -r app/
```

---

Pour plus d'informations, consultez la [documentation utilisateur](README.md) ou le [guide de démarrage rapide](QUICKSTART.md).
