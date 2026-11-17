"""Crée automatiquement les pages du site avec un contenu de départ.

Usage :  python manage.py populate_site
Sans danger si on le relance : il ne remplace jamais ce qui existe déjà.
Tous les textes sont des exemples à remplacer depuis l'admin.
"""
import datetime

from django.core.management.base import BaseCommand

from blog.models import BlogIndexPage, BlogPage
from home.models import HomeFeature, HomePage, HomeService, StandardPage

SERVICES = [
    ("Systèmes et réseaux", "Architecture IT, administration et supervision de vos systèmes et réseaux."),
    ("Cybersécurité et données", "Protection de vos actifs : pare-feu, antivirus, contrôle des accès."),
    ("Infogérance", "Nous prenons en charge votre parc informatique au quotidien."),
    ("Stockage et sauvegarde", "Sauvegardes automatiques et stockage sécurisé de vos fichiers."),
    ("Cloud et virtualisation", "Migration vers le cloud et virtualisation de vos serveurs."),
    ("Identification et traçabilité", "Impression durable et précise pour l'étiquetage et la traçabilité."),
]

FEATURES = [
    ("Support réactif", "Une équipe technique disponible pour vous aider rapidement."),
    ("Solutions sur mesure", "Des installations adaptées à la taille et aux besoins de votre entreprise."),
    ("Matériel de qualité", "Serveurs, réseaux, postes de travail et imprimantes des meilleures marques."),
    ("Accompagnement complet", "Du conseil à l'installation, puis la maintenance au quotidien."),
]

ABOUT = (
    "<p>Wonder Tech est une société de services informatiques basée à Sfax. "
    "Nous accompagnons les entreprises dans le choix, l'installation et la maintenance "
    "de leur matériel et de leurs systèmes.</p>"
    "<p><i>Texte d'exemple : remplacez-le par la présentation officielle de l'entreprise.</i></p>"
)

CONTACT = (
    "<h2>Nos coordonnées</h2>"
    "<p><b>Adresse :</b> Route Mahdia km 2, Sfax 3000, Tunisie</p>"
    "<p><b>Téléphone :</b> +216 22 976 177 / +216 74 235 920</p>"
    "<p><b>Email :</b> contact@wondertech.tn</p>"
    "<h2>Horaires d'ouverture</h2>"
    "<p>Lundi – Vendredi : 08h00 – 18h00<br>Samedi : 09h00 – 13h00<br>Dimanche : fermé</p>"
)

POSTS = [
    ("Pourquoi sauvegarder vos données régulièrement", datetime.date(2026, 11, 3),
     "Une panne ou un virus peut survenir à tout moment : voici pourquoi une sauvegarde est indispensable.",
     "<p>Texte d'exemple. Une sauvegarde régulière protège votre entreprise contre la perte de données.</p>"),
    ("Comment choisir un serveur pour votre entreprise", datetime.date(2026, 10, 20),
     "Les critères essentiels pour choisir un serveur adapté à votre activité.",
     "<p>Texte d'exemple. Nombre d'utilisateurs, stockage, évolutivité : les points à vérifier.</p>"),
    ("5 conseils de cybersécurité pour les PME", datetime.date(2026, 10, 5),
     "Des gestes simples pour réduire les risques de piratage.",
     "<p>Texte d'exemple. Mots de passe, mises à jour, sauvegardes, sensibilisation des équipes.</p>"),
]


def ensure_child(parent, model, slug, **fields):
    """Retourne la page enfant si elle existe, sinon la crée et la publie."""
    existing = parent.get_children().filter(slug=slug).first()
    if existing:
        return existing.specific, False
    page = model(slug=slug, **fields)
    parent.add_child(instance=page)
    page.save_revision().publish()
    return page, True


class Command(BaseCommand):
    help = "Crée les pages du site avec un contenu de départ."

    def handle(self, *args, **options):
        home = HomePage.objects.first()
        if home is None:
            self.stderr.write("Aucune page d'accueil trouvée.")
            return

        about, _ = ensure_child(home, StandardPage, "a-propos", title="À propos", body=ABOUT,
                                intro="Qui sommes-nous ?")
        services, _ = ensure_child(
            home, StandardPage, "services", title="Services",
            intro="Six domaines d'expertise pour gérer votre informatique de bout en bout.",
            body="".join(f"<h3>{t}</h3><p>{d}</p>" for t, d in SERVICES),
        )
        ensure_child(home, StandardPage, "produits", title="Produits",
                     intro="Notre catalogue arrive bientôt.", body="<p>Page temporaire.</p>")
        ensure_child(home, StandardPage, "contact", title="Contact", body=CONTACT,
                     intro="Une question ? Un devis ? Contactez-nous.")

        blog, _ = ensure_child(home, BlogIndexPage, "actualites", title="Actualités",
                               intro="<p>Conseils et nouveautés informatiques.</p>")
        for title, date, intro, body in POSTS:
            ensure_child(blog, BlogPage, title.lower().replace(" ", "-")[:50].strip("-")
                         .replace("é", "e").replace("è", "e").replace("'", ""),
                         title=title, date=date, intro=intro, body=body)

        if not home.services.exists():
            for i, (t, d) in enumerate(SERVICES):
                HomeService.objects.create(page=home, title=t, description=d,
                                           link_page=services, sort_order=i)
        if not home.features.exists():
            for i, (t, d) in enumerate(FEATURES):
                HomeFeature.objects.create(page=home, title=t, description=d, sort_order=i)
        contact = home.get_children().filter(slug="contact").first()
        if contact and not home.cta_button_link:
            home.cta_button_link = contact
        if not home.hero_button_link:
            home.hero_button_link = services
        home.save_revision().publish()

        self.stdout.write(self.style.SUCCESS("Site rempli. Ouvrez http://127.0.0.1:8000"))
