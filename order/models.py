from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from customer.models import Customer
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
    address = models.TextField(max_length=250, null=True, blank=True)

    status = models.CharField(max_length=10, choices=ORDER_STATUS_MAPPING, default="0")

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, related_name="orders")
    creator = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL, related_name="creator_orders")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id:05d}-{self.customer}"


class OrderItem(models.Model):
    code = models.CharField(max_length=10, blank=True, editable=False)
    name = models.CharField(max_length=50, blank=True, editable=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    amount = models.DecimalField(max_digits=8, decimal_places=3, default=0, editable=False)

    product_info = models.JSONField(default=dict)
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=ORDER_ITEM_STATUS_MAPPING, default="0")

    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Inventory, null=True, on_delete=models.SET_NULL, related_name="order_items")

    executor = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL, related_name="executor_order_items"
    )
    creator = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL, related_name="creator_order_items"
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
        if self.amount - value < 0:
            raise ValidationError("Amount cannot be negative.")
        self.amount -= value
        self.save()

    def clean(self):
        if not self.product.visible:
            raise ValidationError("Invalid product.")

    def save(self, *args, **kwargs):
        if self.product and (not self.product_info or self.product_id != self.product_info.get("id")):
            self.name = self.product.name
            self.code = self.product.code
            self.price = self.product.price
            self.product_info = {
                "id": self.product.id,
                "name": self.product.name,
                "code": self.product.code,
                "visible": self.product.visible,
                "price": str(self.product.price),
                "max_price": str(self.product.max_price),
                "unit": self.product.unit,
                "comment": self.product.comment,
                "image_url": self.product.image_url,
                "description": self.product.description,
                "store": self.product.store.name if self.product.store else None,
                "category": self.product.category.path if self.product.category else None,
            }
        self.full_clean()
        super(OrderItem, self).save(*args, **kwargs)
