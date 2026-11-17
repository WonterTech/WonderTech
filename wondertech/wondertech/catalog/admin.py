from django.contrib import admin
from .models import Category, Product, ProductImage, Service

admin.site.site_header = "Wondertech – Administration"
admin.site.site_title = "Wondertech"
admin.site.index_title = "Gestion du site"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "order")
    list_editable = ("order",)
    list_filter = ("parent",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "brand", "is_active", "is_featured")
    list_editable = ("is_active", "is_featured")
    list_filter = ("category", "is_active", "is_featured")
    search_fields = ("name", "brand", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("title",)}
