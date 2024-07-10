import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(
        null=False,
        blank=False,
        max_length=13,
        unique=True,
    )
    additional_data = models.JSONField(null=True, blank=True, default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "customers"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        if not re.match(r"^[0-9]{10,13}$", self.phone_number):
            message = _(
                f"Invalid phone number '{self.phone_number}'. "
                f"Please enter a phone number between 10 and 13 digits long, eg: 987654321"
            )
            raise ValidationError({"phone_number": message})

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.phone_number

        self.full_clean()  # Perform full validation
        super().save(*args, **kwargs)


class Address(models.Model):
    address = models.CharField(max_length=200, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_address")

    class Meta:
        verbose_name_plural = "addresses"

    def __str__(self):
        return self.address
