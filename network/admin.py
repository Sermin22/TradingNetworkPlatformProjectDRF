from django.contrib import admin
from network.models import NetworkLink, Product


@admin.register(NetworkLink)
class NetworkLinkAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "country", "city", "street", "house_number", "network_type",
                    "supplier", "debt_to_supplier", "created_at", "level")
    list_filter = ("city", "country", "created_at")
    search_fields = ("name", "email", "city", "country")


@admin.register(Product)
class ProductkAdmin(admin.ModelAdmin):
    list_display = ("id", "network_link", "name", "model", "release_date")
    list_filter = ("network_link", "name", "release_date")
    search_fields = ("name",)
