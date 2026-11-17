"""Lancez ce script UNE fois depuis le dossier qui contient manage.py :
    python update_step4.py
Il met à jour la base de données (nouveaux champs) puis remplit le contenu manquant."""
import subprocess
import sys

for cmd in (["makemigrations", "home"], ["migrate"], ["populate_site"]):
    print(">> python manage.py", " ".join(cmd))
    if subprocess.call([sys.executable, "manage.py", *cmd]) != 0:
        sys.exit("Une commande a échoué, envoyez-moi le message d'erreur.")
print("\nTerminé ! Lancez : python manage.py runserver  (puis Ctrl+F5 dans le navigateur)")
