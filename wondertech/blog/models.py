from django.db import models
from django.utils import timezone
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index


class BlogIndexPage(Page):
    """Liste des articles (Actualités)."""

    intro = RichTextField("Introduction", blank=True)

    subpage_types = ["blog.BlogPage"]
    content_panels = Page.content_panels + [FieldPanel("intro")]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = BlogPage.objects.child_of(self).live().order_by("-date")
        return context


class BlogPage(Page):
    """Un article."""

    date = models.DateField("Date de publication", default=timezone.localdate)
    intro = models.CharField("Résumé", max_length=250)
    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+", verbose_name="Image",
    )
    body = RichTextField("Contenu")

    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]
    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("image"),
        FieldPanel("body"),
    ]
