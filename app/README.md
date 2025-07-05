# 🌐 Interface Web - Lanceur d'Alerte Suricata

Interface web Flask pour visualiser et gérer les alertes de sécurité Suricata.

## 🚀 Démarrage Rapide

```bash
# Dans le dossier app/
python app.py
```

Puis ouvrez votre navigateur sur : http://localhost:5000

## 📁 Structure des Fichiers

```
app/
├── app.py                 # Application Flask principale
├── prepare_mini_log.py    # Script de préparation des logs
├── merge_rules.py         # Fusion des règles Suricata
├── mini_eve.json          # Cache des logs optimisés
├── user_rules.txt         # Règles personnalisées
└── templates/
    ├── index.html         # Page principale des alertes
    └── rules.html         # Page de gestion des règles
```

## 🛠️ Scripts Utilitaires

### 1. prepare_mini_log.py

**But :** Optimise les logs Suricata pour l'interface web

```bash
python prepare_mini_log.py
```

**Ce qu'il fait :**
- Lit les 5000 dernières lignes de `/var/log/suricata/eve.json`
- Extrait uniquement les alertes (ignore les autres événements)
- Formate les timestamps en français
- Génère `mini_eve.json` pour un chargement rapide

**Configuration :**
- `EVE_LOG_PATH` : Chemin vers le fichier eve.json de Suricata
- `TAIL_LINES` : Nombre de lignes à traiter (défaut : 5000)

### 2. merge_rules.py

**But :** Fusionne les règles personnalisées avec la configuration Suricata

```bash
sudo python merge_rules.py
```

**Ce qu'il fait :**
- Sauvegarde l'ancien fichier de règles
- Copie les règles de `user_rules.txt` vers `/etc/suricata/rules/local.rules`
- Permet d'appliquer vos règles personnalisées

⚠️ **Privilèges requis :** Ce script nécessite sudo car il modifie des fichiers système.

## 🌐 Interface Web

### Page Principale (`/`)

**Fonctionnalités :**
- **Vue par catégories** : Alertes regroupées par signature
- **Filtrage par date** : Sélecteur de date avec calendrier
- **Chargement paresseux** : Affichage initial limité, puis chargement complet sur demande
- **Cache intelligent** : Mise à jour automatique toutes les 30 secondes

**Utilisation :**
1. Les alertes sont groupées par type (signature)
2. Cliquez sur une catégorie pour voir un aperçu
3. Utilisez "Charger tous les logs" pour voir tous les détails
4. Filtrez par date avec le sélecteur en haut

### Page des Règles (`/rules`)

**Fonctionnalités :**
- **Visualisation** : Affiche les règles utilisateur et locales
- **Ajout simple** : Formulaire pour créer des règles basiques
- **Édition manuelle** : Zone de texte pour règles avancées

**Types de règles supportées :**
- **TCP/UDP/ICMP** : Protocoles de base
- **Ports spécifiques** : Filtrage par port de destination
- **Messages personnalisés** : Descriptions d'alertes

## ⚙️ Configuration

### Variables dans app.py

```python
# Chemins des fichiers
MINI_LOG_PATH = "mini_eve.json"          # Cache des logs
USER_RULES_PATH = "user_rules.txt"       # Règles personnalisées
DEFAULT_LOGS_PER_CATEGORY = 20           # Logs affichés par défaut
CACHE_REFRESH_INTERVAL = 30              # Secondes entre les refreshes
```

### Personnalisation du Serveur

```python
# En bas de app.py
app.run(host="0.0.0.0", port=5000)
```

**Options :**
- `host="127.0.0.1"` : Accès local uniquement
- `host="0.0.0.0"` : Accès depuis le réseau (défaut)
- `port=5000` : Port d'écoute (modifiable)
- `debug=True` : Mode debug pour le développement

## 📊 Gestion des Données

### Cache des Logs

Le système utilise un cache en mémoire pour optimiser les performances :

```python
logs_cache = {
    "all_logs": [],      # Tous les logs chargés
    "last_update": 0,    # Timestamp de la dernière MAJ
    "dates": []          # Dates disponibles pour le filtre
}
```

**Avantages :**
- Chargement rapide de l'interface
- Réduction des accès disque
- Filtrage efficace par date

### Format des Logs

Chaque log dans `mini_eve.json` contient :

```json
{
    "signature": "Nom de l'alerte",
    "src_ip": "IP source",
    "dest_ip": "IP destination", 
    "timestamp": "2025-07-05T10:30:00.000Z",
    "formatted_time": "5 juillet 2025, 10:30:00",
    "date_only": "2025-07-05"
}
```

## 🎨 Personnalisation de l'Interface

### CSS Personnalisé

Les templates utilisent du CSS intégré. Pour personnaliser :

1. Éditez les styles dans `templates/index.html` et `templates/rules.html`
2. Ou créez un fichier CSS externe dans un dossier `static/`

### Thèmes Disponibles

**Thème actuel :** Mode sombre avec accents bleus
- Fond principal : `#f0f2f5`
- Cartes : `#343a40` (sombre)
- Boutons : `#007bff` (bleu)

## 🔧 API Endpoints

### GET /

Page principale avec liste des alertes par catégorie

**Paramètres :**
- `date` (optionnel) : Filtre par date (format YYYY-MM-DD)

### GET /load_all

Charge tous les logs pour une signature donnée

**Paramètres :**
- `signature` (requis) : Nom de la signature
- `date` (optionnel) : Filtre par date

**Réponse :** HTML des logs détaillés

### GET/POST /rules

- **GET** : Affiche la page de gestion des règles
- **POST** : Ajoute une nouvelle règle

**Paramètres POST :**
- `protocol` : tcp/udp/icmp
- `port` (optionnel) : Port de destination
- `message` : Description de l'alerte

## 🐛 Debugging

### Problèmes de Performance

1. **Chargement lent** : Réduisez `TAIL_LINES` dans `prepare_mini_log.py`
2. **Mémoire élevée** : Diminuez `DEFAULT_LOGS_PER_CATEGORY`
3. **Cache obsolète** : Supprimez `mini_eve.json` pour forcer la régénération

### Logs de Debug

Activez le mode debug :

```python
app.run(host="0.0.0.0", port=5000, debug=True)
```

**Avantages du mode debug :**
- Rechargement automatique lors des modifications
- Messages d'erreur détaillés
- Console de debug intégrée

### Vérification des Fichiers

```bash
# Vérifier la génération des logs
ls -la mini_eve.json

# Vérifier les règles utilisateur
cat user_rules.txt

# Tester la préparation des logs
python prepare_mini_log.py
```

## 📚 Exemples d'Utilisation

### Ajout de Règles Personnalisées

**Via l'interface web :**
1. Allez sur `/rules`
2. Remplissez le formulaire simple
3. Ou ajoutez des règles avancées dans la zone de texte

**Règles avancées dans user_rules.txt :**

```bash
# Détection de brute force SSH
alert tcp any any -> $HOME_NET 22 (msg:"SSH Brute Force"; threshold:type both, track by_src, count 5, seconds 300; sid:1000001;)

# Détection de scan de ports
alert tcp any any -> $HOME_NET any (msg:"Port Scan"; flags:S; threshold:type both, track by_src, count 10, seconds 60; sid:1000002;)

# Détection de trafic DNS suspect
alert udp any any -> any 53 (msg:"DNS Query Suspect"; content:"malware"; nocase; sid:1000003;)
```

### Filtrage et Recherche

**Par date :**
- Utilisez le calendrier sur la page principale
- Format : YYYY-MM-DD

**Par signature :**
- Les alertes sont automatiquement groupées
- Cliquez sur une catégorie pour l'explorer

### Maintenance Régulière

```bash
# Actualiser les logs (toutes les heures par exemple)
0 * * * * cd /chemin/vers/app && python prepare_mini_log.py

# Nettoyer les anciens logs (une fois par semaine)
find . -name "mini_eve.json" -mtime +7 -delete
```

## 🚀 Optimisations Recommandées

1. **Production** : Utilisez un serveur WSGI (Gunicorn, uWSGI)
2. **Base de données** : Remplacez JSON par SQLite/PostgreSQL pour de gros volumes
3. **Monitoring** : Ajoutez des métriques avec Prometheus/Grafana
4. **Sécurité** : Implémentez l'authentification pour un accès public

---

Pour retourner au projet principal, consultez le [README principal](../README.md).
