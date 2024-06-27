from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from account.models import Address


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    model = get_user_model()
    list_display = ("username", "email", "phone_number", "first_name", "is_staff")
    list_display_links = ("username", "email")
    list_filter = ("is_active", "is_staff", "is_superuser", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("id", "is_staff")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "phone_number")}),
        ("Additional Details", {"fields": ("additional_data",)}),
        (
            "Permissions",
            {
                "classes": ("collapse",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {"classes": ("wide",), "fields": ("username", "email", "password1", "password2")},
        ),
    )
    readonly_fields = ("date_joined",)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(BaseUserAdmin, self).get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            readonly_fields += ("is_staff", "is_superuser")

            if not obj:
                return readonly_fields

            if obj.is_superuser or (obj.is_staff and request.user.pk != obj.pk):
                readonly_fields += ("username", "password", "email", "is_active", "groups")

        return readonly_fields


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "address", "user")
    list_display_links = ("id",)
    search_fields = list_display
    list_filter = ("address", "user")
