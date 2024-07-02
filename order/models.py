from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from inventory.models import Inventory

ORDER_STATUS_MAPPING = [
    ("0", "pending"),
    ("1", "in_progress"),
    ("2", "delivered"),
    ("3", "cancelled"),
]

ORDER_ITEM_STATUS_MAPPING = [
    ("0", "pending"),
    ("1", "in_progress"),
    ("2", "completed"),
    ("3", "cancelled"),
]


class Order(models.Model):
    address = models.CharField(max_length=200, null=True, blank=True)

    status = models.CharField(max_length=5, choices=ORDER_STATUS_MAPPING, default="0")

    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL, related_name="user")
    created_by = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL, related_name="order_created_by"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"ORDER{self.id:05d}"

    @property
    def items(self):
        return self.order_item.all()


class OrderItem(models.Model):
    code = models.CharField(max_length=10, blank=True, editable=False)
    name = models.CharField(max_length=50, blank=True, editable=False)
    unit = models.CharField(max_length=5, blank=True, editable=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    amount = models.DecimalField(max_digits=8, decimal_places=3, default=0, editable=False)

    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=5, choices=ORDER_ITEM_STATUS_MAPPING, default="0")

    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name="order_item")
    product = models.ForeignKey(Inventory, null=True, on_delete=models.SET_NULL, related_name="product")

    assign_to = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL, related_name="order_item_assign_to"
    )
    created_by = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL, related_name="order_item_created_by"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "order items"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order}-{self.name}"

    def increment_amount(self, value):
        if value < 0:
            raise ValidationError("Increment value must be non-negative.")
        self.amount += value
        self.save()

    def decrement_amount(self, value):
        if value < 0:
            raise ValidationError("Decrement value must be non-negative.")
        if (self.amount - value) < 0:
            raise ValidationError("Amount cannot be negative.")
        self.amount -= value
        self.save()

    def save(self, *args, **kwargs):
        if not self.product.visible:
            raise ValidationError("Invalid product.")

        if self.product:
            self.name = self.product.name
            self.code = self.product.code
            self.unit = self.product.unit
            self.price = self.product.price

        super(OrderItem, self).save(*args, **kwargs)
