# 🚀 Guide de Démarrage Rapide - Lanceur d'Alerte Suricata

Ce guide vous permettra de démarrer rapidement avec le système de monitoring des alertes Suricata.

## ⚡ Installation Express (5 minutes)

### 1. Prérequis

```bash
# Vérifier Python (3.6+ requis)
python --version

# Installer les dépendances
pip install flask python-dateutil
```

### 2. Configuration Suricata

Assurez-vous que Suricata fonctionne et génère des logs :

```bash
# Vérifier le statut de Suricata
sudo systemctl status suricata

# Vérifier que les logs sont générés
ls -la /var/log/suricata/eve.json
```

Si le fichier n'existe pas, adaptez le chemin dans les scripts Python.

### 3. Premier Démarrage

```bash
# Cloner ou télécharger le projet
cd lanceur_alerte/

# Générer le cache des logs
cd app/
python prepare_mini_log.py

# Lancer l'interface web
python app.py
```

### 4. Accéder à l'Interface

Ouvrez votre navigateur sur : **http://localhost:5000**

## 🎯 Utilisation Immédiate

### Interface Web

1. **Page principale** : Visualisez les alertes par catégorie
2. **Filtrage** : Utilisez le sélecteur de date
3. **Gestion des règles** : Cliquez sur "⚙️ Gérer les règles"

### Surveillance Temps Réel

Dans un nouveau terminal :

```bash
# Démarrer les notifications en temps réel
python lanceur_alerte.py
```

## 🔧 Configuration Rapide pour Windows

### Installation Python et Dépendances

```powershell
# Installer les dépendances via pip
pip install flask python-dateutil

# Si vous utilisez conda
conda install flask python-dateutil
```

### Adaptation des Chemins

Modifiez les chemins dans les fichiers Python pour Windows :

**Dans `prepare_mini_log.py`** :
```python
# Remplacez cette ligne
EVE_LOG_PATH = "/var/log/suricata/eve.json"

# Par le chemin Windows de vos logs Suricata
EVE_LOG_PATH = r"C:\Program Files\Suricata\logs\eve.json"
```

**Dans `merge_rules.py`** :
```python
# Adaptez ces chemins pour Windows
LOCAL_RULES = r"C:\Program Files\Suricata\rules\local.rules"
BACKUP_RULES = r"C:\Program Files\Suricata\rules\local.rules.bak"
```

## 🛠️ Résolution de Problèmes Courants

### Problème 1 : Fichier eve.json introuvable

**Symptôme :** Erreur "Fichier eve.json non trouvé"

**Solution :**
```bash
# Trouvez votre fichier de logs Suricata
find /var/log -name "eve.json" 2>/dev/null

# Ou sous Windows
dir "eve.json" /s
```

Puis modifiez le chemin dans `prepare_mini_log.py`.

### Problème 2 : Interface web inaccessible

**Symptôme :** Impossible d'accéder à http://localhost:5000

**Solutions :**
1. Vérifiez que Flask démarre sans erreur
2. Testez un autre port :
   ```python
   app.run(host="0.0.0.0", port=8080)
   ```
3. Vérifiez le firewall

### Problème 3 : Pas de notifications

**Symptôme :** Le script fonctionne mais pas de notifications

**Solutions :**
- **Linux** : Installez `libnotify-bin`
  ```bash
  sudo apt-get install libnotify-bin
  ```
- **Windows** : Les notifications ne sont pas supportées par défaut

### Problème 4 : Erreurs de permissions

**Symptôme :** Accès refusé aux fichiers de logs

**Solutions :**
```bash
# Ajouter votre utilisateur au groupe suricata
sudo usermod -a -G suricata $USER

# Ou donner des permissions de lecture
sudo chmod 644 /var/log/suricata/eve.json
```

## 📝 Test avec des Données Factices

Si vous n'avez pas encore de logs Suricata, vous pouvez tester avec des données factices :

1. **Créer des logs de test** :
   ```bash
   python generate_test_logs.py
   ```

2. **Modifier le chemin temporairement** dans `prepare_mini_log.py` :
   ```python
   EVE_LOG_PATH = "test_eve.json"  # au lieu du chemin Suricata
   ```

3. **Exécuter la préparation** :
   ```bash
   python prepare_mini_log.py
   ```

## 🔍 Vérifications Post-Installation

### 1. Vérifier les Fichiers Générés

```bash
# Dans le dossier app/
ls -la mini_eve.json user_rules.txt
```

### 2. Tester l'Interface Web

1. Ouvrez http://localhost:5000
2. Vérifiez que les alertes s'affichent
3. Testez le filtrage par date
4. Accédez à la page des règles

### 3. Tester les Notifications

```bash
# Tester notify-send (Linux uniquement)
notify-send "Test" "Les notifications fonctionnent !"
```

## ⚡ Commandes Utiles

### Surveillance des Logs

```bash
# Voir les logs Suricata en temps réel
tail -f /var/log/suricata/eve.json

# Compter les alertes du jour
grep "$(date '+%Y-%m-%d')" /var/log/suricata/eve.json | grep '"event_type":"alert"' | wc -l
```

### Gestion du Service

```bash
# Redémarrer Suricata
sudo systemctl restart suricata

# Voir les erreurs Suricata
sudo journalctl -u suricata -f
```

### Debug Flask

```bash
# Lancer Flask en mode debug
export FLASK_DEBUG=1
python app.py
```

## 📞 Support Rapide

### Erreurs Fréquentes

| Erreur | Solution Rapide |
|--------|----------------|
| `Module 'flask' not found` | `pip install flask` |
| `Permission denied` | Vérifier les droits sur `/var/log/suricata/` |
| `Address already in use` | Tuer le processus : `kill $(lsof -ti:5000)` |
| `File not found` | Adapter les chemins dans les scripts |

### Logs de Debug

Pour diagnostiquer :

```bash
# Debug prepare_mini_log.py
python -c "
import os
print('eve.json exists:', os.path.exists('/var/log/suricata/eve.json'))
print('eve.json readable:', os.access('/var/log/suricata/eve.json', os.R_OK))
"

# Debug app.py
python -c "
import sys
sys.path.append('app')
from app import load_mini_logs
print('mini_eve.json loaded successfully')
"
```

## 🎯 Prochaines Étapes

Une fois l'installation terminée :

1. **Personnalisez les règles** via l'interface web
2. **Configurez le démarrage automatique** avec systemd
3. **Explorez les logs** pour comprendre votre trafic réseau
4. **Ajustez les seuils** d'alerte selon vos besoins

---

**Temps total d'installation : 5-10 minutes** ⏱️

Pour plus de détails, consultez le [README principal](README.md) et le [README de l'application](app/README.md).
