from .models import Category, Service


def nav_menu(request):
    """Données des menus déroulants (Services / Produits) pour base.html."""
    return {
        "nav_categories": Category.objects.filter(parent=None).prefetch_related("children"),
        "nav_services": Service.objects.all(),
    }
