from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Product, Service


def _paginate(request, queryset, per_page=12):
    return Paginator(queryset, per_page).get_page(request.GET.get("page"))


def product_list(request):
    products = Product.objects.filter(is_active=True).select_related("category")
    return render(request, "catalog/product_list.html", {
        "page": _paginate(request, products),
        "categories": Category.objects.filter(parent=None),
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    cats = [category, *category.children.all()]
    products = Product.objects.filter(is_active=True, category__in=cats)
    return render(request, "catalog/category_detail.html", {
        "category": category,
        "subcategories": category.children.all(),
        "page": _paginate(request, products),
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = (Product.objects.filter(is_active=True, category=product.category)
               .exclude(pk=product.pk)[:4])
    return render(request, "catalog/product_detail.html",
                  {"product": product, "related": related})


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, "catalog/service_detail.html", {"service": service})


def search(request):
    q = request.GET.get("q", "").strip()
    results = Product.objects.none()
    if q:
        results = Product.objects.filter(is_active=True).filter(
            Q(name__icontains=q) | Q(brand__icontains=q)
            | Q(short_description__icontains=q) | Q(description__icontains=q)
            | Q(category__name__icontains=q)
        ).distinct()
    return render(request, "catalog/search.html", {
        "q": q, "page": _paginate(request, results),
    })
