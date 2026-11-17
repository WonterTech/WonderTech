"""Lancez ce script UNE fois depuis le dossier qui contient manage.py :
    python install.py
Il ajoute l'app "blog" aux réglages, puis met à jour la base de données."""
import pathlib
import subprocess
import sys

settings = pathlib.Path("wondertech/settings/base.py")
if not settings.exists():
    sys.exit("Erreur : lancez ce script depuis le dossier qui contient manage.py")

text = settings.read_text(encoding="utf-8")
if '"blog"' in text:
    print("OK : l'app blog est déjà dans INSTALLED_APPS")
elif '"home",' in text:
    settings.write_text(text.replace('"home",', '"home",\n    "blog",', 1), encoding="utf-8")
    print("OK : app blog ajoutée dans INSTALLED_APPS")
else:
    sys.exit('Erreur : ajoutez "blog", à INSTALLED_APPS à la main dans ' + str(settings))

for cmd in (["makemigrations", "home", "blog"], ["migrate"]):
    print(">> python manage.py", " ".join(cmd))
    if subprocess.call([sys.executable, "manage.py", *cmd]) != 0:
        sys.exit("Une commande a échoué, envoyez-moi le message d'erreur.")

print("\nTerminé ! Lancez : python manage.py runserver")
