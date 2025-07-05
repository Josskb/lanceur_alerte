# 🚨 Lanceur d'Alerte Suricata

Un système de monitoring et d'interface web pour visualiser et gérer les alertes de sécurité Suricata en temps réel.

## 📋 Description

Ce projet propose une solution complète pour :
- **Surveiller** les alertes Suricata en temps réel
- **Visualiser** les logs d'alertes dans une interface web moderne
- **Gérer** les règles Suricata personnalisées
- **Recevoir** des notifications système pour les alertes critiques

## 🏗️ Architecture

```
lanceur_alerte/
├── lanceur_alerte.py          # Surveillance temps réel et notifications
├── app/
│   ├── app.py                 # Application web Flask
│   ├── prepare_mini_log.py    # Traitement des logs Suricata
│   ├── merge_rules.py         # Fusion des règles personnalisées
│   ├── mini_eve.json          # Cache des logs traités
│   ├── user_rules.txt         # Règles personnalisées
│   └── templates/
│       ├── index.html         # Interface principale
│       └── rules.html         # Gestion des règles
└── README.md
```

## 🚀 Installation

### Prérequis

- Python 3.6+
- Suricata installé et configuré
- Flask et dépendances Python

### Installation des dépendances

```bash
pip install flask python-dateutil
```

### Configuration Suricata

Assurez-vous que Suricata écrit ses logs JSON dans `/var/log/suricata/eve.json`.

## 📖 Utilisation

### 1. Surveillance en temps réel

Pour démarrer la surveillance en temps réel avec notifications :

```bash
python3 lanceur_alerte.py
```

**Fonctionnalités :**
- Surveille le fichier eve.json de Suricata
- Envoie des notifications système pour chaque nouvelle alerte
- Anti-spam : évite les notifications répétées (cooldown de 30s)

### 2. Interface Web

Pour lancer l'interface web de visualisation :

```bash
cd app/
python3 app.py
```

Puis ouvrez votre navigateur sur : `http://localhost:5000`

**Fonctionnalités de l'interface :**
- 📊 **Dashboard principal** : Visualisation des alertes par catégorie
- 📅 **Filtrage par date** : Sélection de dates spécifiques
- 🔍 **Détails des alertes** : IP source/destination, timestamps
- ⚙️ **Gestion des règles** : Ajout de règles personnalisées

### 3. Préparation des logs

Pour traiter et optimiser les logs Suricata :

```bash
cd app/
python3 prepare_mini_log.py
```

Cette commande :
- Lit les dernières 5000 lignes du fichier eve.json
- Extrait uniquement les alertes
- Génère un fichier mini_eve.json optimisé pour l'interface web

### 4. Fusion des règles

Pour appliquer les règles personnalisées à Suricata :

```bash
cd app/
python3 merge_rules.py
```

⚠️ **Attention :** Cette commande nécessite des privilèges administrateur car elle modifie `/etc/suricata/rules/local.rules`.

## 🔧 Configuration

### Chemins des fichiers

Les chemins par défaut peuvent être modifiés dans les fichiers Python :

- **Logs Suricata** : `/var/log/suricata/eve.json`
- **Règles locales** : `/etc/suricata/rules/local.rules`
- **Règles utilisateur** : `app/user_rules.txt`
- **Cache logs** : `app/mini_eve.json`

### Interface Web - Port et Host

Par défaut, l'application web écoute sur :
- **Host** : `0.0.0.0` (accessible depuis le réseau)
- **Port** : `5000`

Pour modifier, éditez la ligne dans `app/app.py` :
```python
app.run(host="0.0.0.0", port=5000)
```

## 📊 Utilisation de l'Interface Web

### Page principale (`/`)

1. **Vue par catégories** : Les alertes sont regroupées par signature
2. **Filtrage temporel** : Utilisez le sélecteur de date pour filtrer
3. **Chargement détaillé** : Cliquez sur "Charger tous les logs" pour voir tous les détails

### Gestion des règles (`/rules`)

1. **Visualisation** : Consultez les règles existantes
2. **Ajout simple** : Utilisez le formulaire pour créer des règles basiques
3. **Règles avancées** : Ajoutez des règles complexes dans la zone de texte

#### Exemple de règles personnalisées

```
# Détection de scan de ports
alert tcp any any -> $HOME_NET any (msg:"Scan de ports détecté"; flags:S; threshold:type both, track by_src, count 10, seconds 60; sid:1000001;)

# Détection de tentative de connexion SSH répétée
alert tcp any any -> $HOME_NET 22 (msg:"Tentatives SSH multiples"; threshold:type both, track by_src, count 5, seconds 300; sid:1000002;)
```

## 🔍 Fonctionnalités Avancées

### Cache et Performance

- **Cache automatique** : Les logs sont mis en cache pour améliorer les performances
- **Actualisation** : Le cache se renouvelle toutes les 30 secondes
- **Optimisation** : Seuls les logs d'alerte sont traités (pas les autres événements Suricata)

### Anti-spam des Notifications

Le système de notifications intègre un mécanisme anti-spam :
- Une même alerte ne peut déclencher qu'une notification toutes les 30 secondes
- Évite la pollution du système de notifications

## 🛠️ Démarrage Automatique

### Systemd (Linux)

Créez un service systemd pour démarrer automatiquement :

```bash
sudo nano /etc/systemd/system/lanceur-alerte.service
```

Contenu du fichier :
```ini
[Unit]
Description=Lanceur d'Alerte Suricata
After=network.target

[Service]
Type=simple
User=votre-utilisateur
WorkingDirectory=/chemin/vers/lanceur_alerte
ExecStart=/usr/bin/python3 lanceur_alerte.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Activez le service :
```bash
sudo systemctl enable lanceur-alerte.service
sudo systemctl start lanceur-alerte.service
```

## 🐛 Dépannage

### Problèmes courants

1. **Fichier eve.json introuvable**
   - Vérifiez que Suricata fonctionne : `sudo systemctl status suricata`
   - Vérifiez le chemin dans les scripts Python

2. **Permissions insuffisantes**
   - Pour merge_rules.py : `sudo python3 merge_rules.py`
   - Pour accéder aux logs : ajoutez votre utilisateur au groupe suricata

3. **Interface web inaccessible**
   - Vérifiez que le port 5000 n'est pas bloqué
   - Consultez les logs Flask dans le terminal

4. **Pas de notifications**
   - Vérifiez que `notify-send` est installé
   - Testez : `notify-send "Test" "Message de test"`

### Logs de débogage

Pour activer le mode debug Flask, modifiez `app.py` :
```python
app.run(host="0.0.0.0", port=5000, debug=True)
```

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## 📞 Support

Pour toute question ou problème, créez une issue sur le repository du projet.

---

**Note :** Ce projet est conçu pour des environnements de développement et de test. Pour un usage en production, assurez-vous d'implémenter des mesures de sécurité supplémentaires.