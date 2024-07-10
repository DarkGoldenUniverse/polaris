from django.contrib import admin

from customer.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["id", "address", "customer"]
    list_display_links = ["id"]
    search_fields = list_display
    list_filter = ["address", "customer"]
