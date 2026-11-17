from django.urls import path
from . import views

urlpatterns = [
    path("produits/", views.product_list, name="product_list"),
    path("produits/categorie/<slug:slug>/", views.category_detail, name="category_detail"),
    path("produits/<slug:slug>/", views.product_detail, name="product_detail"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("recherche/", views.search, name="search"),
]
