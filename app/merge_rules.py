import shutil

USER_RULES = "/home/joss/lanceur_alerte/app/user_rules.txt"
LOCAL_RULES = "/etc/suricata/rules/local.rules"
BACKUP_RULES = "/etc/suricata/rules/local.rules.bak"

def merge_rules():
    # Sauvegarder l'ancien fichier
    shutil.copy(LOCAL_RULES, BACKUP_RULES)

    with open(LOCAL_RULES, "w") as out_f:
        # Ajouter les règles utilisateur
        if os.path.exists(USER_RULES):
            with open(USER_RULES, "r") as user_f:
                user_rules_content = user_f.read()
                out_f.write(user_rules_content.strip() + "\n")

    print("✅ Règles fusionnées et sauvegardées !")

if __name__ == "__main__":
    merge_rules()
