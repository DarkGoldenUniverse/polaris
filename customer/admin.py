from django.contrib import admin

from customer.models import Address, Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "phone_number"]
    list_display_links = ["id"]
    search_fields = list_display


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["id", "address", "customer"]
    list_display_links = ["id"]
    search_fields = list_display
