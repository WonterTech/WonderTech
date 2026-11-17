from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField("Nom", max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE,
        related_name="children", verbose_name="Catégorie parente",
        help_text="Laisser vide pour une catégorie principale.",
    )
    image = models.ImageField(upload_to="categories/", blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField("Ordre", default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "catégorie"
        verbose_name_plural = "catégories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.parent.name} › {self.name}" if self.parent else self.name

    def get_absolute_url(self):
        return reverse("category_detail", args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products",
        verbose_name="Catégorie",
    )
    name = models.CharField("Nom", max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    brand = models.CharField("Marque", max_length=100, blank=True)
    short_description = models.CharField("Description courte", max_length=250, blank=True)
    description = models.TextField("Description", blank=True)
    specifications = models.TextField(
        "Caractéristiques", blank=True, help_text="Une caractéristique par ligne.",
    )
    is_active = models.BooleanField("Visible sur le site", default=True)
    is_featured = models.BooleanField("Mis en avant", default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "produit"
        verbose_name_plural = "produits"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.slug])

    @property
    def main_image(self):
        return self.images.first()

    @property
    def spec_lines(self):
        return [l.strip() for l in self.specifications.splitlines() if l.strip()]


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField("Texte alternatif", max_length=200, blank=True)
    order = models.PositiveIntegerField("Ordre", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "image"
        verbose_name_plural = "images"


class Service(models.Model):
    title = models.CharField("Titre", max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.CharField("Résumé", max_length=250, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField("Icône", max_length=50, blank=True)
    order = models.PositiveIntegerField("Ordre", default=0)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "service"
        verbose_name_plural = "services"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
