from django import forms
from django.contrib import admin

from inventory.models import Category, Inventory, Store


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        parent = cleaned_data.get("parent")

        # Generate path for the current category
        if parent:
            path = f"{parent.path}.{name}"
        else:
            path = name

        # Check if a category with the same path exists
        if Category.objects.filter(path=path).exclude(pk=self.instance.pk).exists():
            self.add_error("name", f'A category with the name "{path}" already exists.')

        return cleaned_data


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ["id", "path", "name", "parent"]
    list_display_links = ["path"]
    search_fields = list_display
    list_filter = ["path"]


@admin.register(Store)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


class InventoryAdminForm(forms.ModelForm):
    amount_change = forms.DecimalField(
        max_digits=8,
        decimal_places=3,
        required=False,
        initial=0,
        label="Change Amount",
        help_text="Enter a positive value to increment or a negative value to decrement the amount.",
    )
    executed_amount_change = forms.DecimalField(
        max_digits=8,
        decimal_places=3,
        required=False,
        initial=0,
        label="Change Executed Amount",
        help_text="Enter a positive value to increment or a negative value to decrement the executed amount.",
    )

    class Meta:
        model = Inventory
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)

        amount_change = self.cleaned_data["amount_change"]
        executed_amount_change = self.cleaned_data["executed_amount_change"]

        if amount_change > 0:
            instance.increment_amount(amount_change)
        elif amount_change < 0:
            instance.decrement_amount(-1 * amount_change)
        if executed_amount_change > 0:
            instance.increment_amount(executed_amount_change)
        elif executed_amount_change < 0:
            instance.decrement_amount(-1 * executed_amount_change)

        if commit:
            instance.save()
        return instance


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    form = InventoryAdminForm
    list_display = ["id", "code", "name", "category", "visible", "price", "amount", "executed_amount"]
    list_display_links = ["code", "name"]
    search_fields = ["code", "name", "category"]
    list_filter = ["visible", "store", "category"]
    fieldsets = [
        ("Basic Detail", {"classes": ["wide"], "fields": ["visible", "code", "name", "store", "category"]}),
        (
            "Price and Amount Detail",
            {
                "classes": ["wide"],
                "fields": [
                    "max_price",
                    "price",
                    "unit",
                    "amount",
                    "amount_change",
                    "executed_amount",
                    "executed_amount_change",
                ],
            },
        ),
        ("Additional Details", {"classes": ["collapse"], "fields": ["image_url", "comment", "description"]}),
    ]
    readonly_fields = ["amount", "executed_amount"]
