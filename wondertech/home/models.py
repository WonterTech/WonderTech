from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page


class HomePage(Page):
    """Page d'accueil : tout le texte se modifie dans l'admin."""

    hero_title = models.CharField(
        "Titre de la bannière", max_length=200,
        default="Gamme complète de services informatiques et de vente de matériel",
    )
    hero_subtitle = models.CharField(
        "Sous-titre", max_length=250, blank=True,
        default="Infrastructure, sécurité et support technique sur mesure",
    )
    hero_button_text = models.CharField(
        "Texte du bouton", max_length=60, blank=True, default="Découvrir nos solutions"
    )
    hero_button_link = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+", verbose_name="Page du bouton",
    )
    hero_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+", verbose_name="Image de fond de la bannière",
    )
    services_title = models.CharField("Titre section services", max_length=100, default="Nos services")
    services_intro = models.CharField(
        "Introduction services", max_length=250, blank=True,
        default="Des domaines d'expertise pour gérer votre informatique de bout en bout.",
    )
    features_title = models.CharField(
        "Titre section « Pourquoi nous »", max_length=100, default="Pourquoi choisir Wonder Tech ?"
    )
    cta_title = models.CharField("Bandeau final : titre", max_length=120, default="Un projet ? Parlons-en.")
    cta_text = models.CharField(
        "Bandeau final : texte", max_length=250, blank=True,
        default="Demandez votre devis gratuit, nous vous répondons sous 24 h.",
    )
    cta_button_text = models.CharField("Bandeau final : texte du bouton", max_length=60, default="Demander un devis")
    cta_button_link = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+", verbose_name="Bandeau final : page du bouton",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_subtitle"),
                FieldPanel("hero_button_text"),
                FieldPanel("hero_button_link"),
                FieldPanel("hero_image"),
            ],
            heading="Bannière",
        ),
        MultiFieldPanel(
            [FieldPanel("services_title"), FieldPanel("services_intro")],
            heading="Section services",
        ),
        InlinePanel("services", label="Service"),
        FieldPanel("features_title"),
        InlinePanel("features", label="Point fort"),
        MultiFieldPanel(
            [
                FieldPanel("cta_title"),
                FieldPanel("cta_text"),
                FieldPanel("cta_button_text"),
                FieldPanel("cta_button_link"),
            ],
            heading="Bandeau final (appel à l'action)",
        ),
    ]


class HomeService(Orderable):
    """Une carte de service sur l'accueil (on peut en ajouter, supprimer, réordonner)."""

    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="services")
    title = models.CharField("Titre", max_length=100)
    description = models.TextField("Description", blank=True)
    link_page = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+", verbose_name="Lien (optionnel)",
    )

    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+", verbose_name="Image (optionnelle)",
    )

    panels = [
        FieldPanel("title"), FieldPanel("description"),
        FieldPanel("image"), FieldPanel("link_page"),
    ]


class HomeFeature(Orderable):
    """Un point fort (section « Pourquoi nous choisir »)."""

    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="features")
    title = models.CharField("Titre", max_length=100)
    description = models.TextField("Description", blank=True)

    panels = [FieldPanel("title"), FieldPanel("description")]


class StandardPage(Page):
    """Page de texte simple : À propos, Services, Conditions, etc."""

    intro = models.CharField("Introduction", max_length=300, blank=True)
    header_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+", verbose_name="Image d'en-tête (optionnelle)",
    )
    body = RichTextField("Contenu", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"), FieldPanel("header_image"), FieldPanel("body"),
    ]
