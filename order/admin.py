from django import forms
from django.contrib import admin

from inventory.models import Inventory
from order.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "status"]
    list_display_links = ["id", "customer"]
    search_fields = list_display
    list_filter = ["status"]
    readonly_fields = ["created_at", "updated_at"]


class OrderItemAdminForm(forms.ModelForm):
    amount_change = forms.DecimalField(
        max_digits=8,
        decimal_places=3,
        required=True,
        initial=0,
        label="Change Amount",
        help_text="Enter a positive value to increment or a negative value to decrement the amount.",
    )
    product = forms.ModelChoiceField(queryset=Inventory.objects.filter(visible=True))

    class Meta:
        model = OrderItem
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)

        amount_change = self.cleaned_data["amount_change"]

        if amount_change > 0:
            instance.increment_amount(amount_change)
        elif amount_change < 0:
            instance.decrement_amount(-1 * amount_change)

        if commit:
            instance.save()
        return instance


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    form = OrderItemAdminForm
    list_display = [
        "id",
        "order",
        "code",
        "name",
        "price",
        "amount",
        "status",
        "executor",
    ]
    list_display_links = ["order", "code", "name"]
    search_fields = list_display
    list_filter = ["status"]
    readonly_fields = ["code", "name", "price", "amount", "unit", "created_at", "updated_at"]
    fieldsets = [
        ("Basic Detail", {"fields": ["status", "order", "product", "amount_change"]}),
        ("Product Detail", {"fields": ["code", "name", "price", "amount", "unit"]}),
        ("Additional Details", {"fields": ["executor", "creator", "created_at", "updated_at"]}),
    ]
