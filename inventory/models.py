from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models

UNIT_MAPPING = [
    ("kg", "Kg"),
    ("g", "gram"),
    ("l", "L"),
    ("ml", "mL"),
    ("p", "Pack"),
]


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        validators=[
            validators.RegexValidator(
                regex=r"^[a-z0-9_]{3,50}$",
                message="Name must contain at least three alphanumeric characters (a-z, 0-9, _).",
            )
        ],
    )

    path = models.CharField(max_length=255, blank=True, editable=False, unique=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children")

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.path

    def clean(self):
        self.name = (self.name or "").lower()
        super(Category, self).clean()

    def save(self, *args, **kwargs):
        # Generate and set the path for the category
        if self.parent:
            self.path = f"{self.parent.path}.{self.name}"
        else:
            self.path = self.name
        super(Category, self).save(*args, **kwargs)


class Store(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "stores"

    def __str__(self):
        return self.name


class Inventory(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    visible = models.BooleanField(default=False)

    max_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        validators=[validators.MinValueValidator(0)],
        verbose_name="Maximum Price (MRP)",
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        validators=[validators.MinValueValidator(0)],
        verbose_name="Selling Price",
    )
    amount = models.DecimalField(
        max_digits=8, decimal_places=3, default=0, validators=[validators.MinValueValidator(0)], verbose_name="Amount"
    )
    executed_amount = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        default=0,
        validators=[validators.MinValueValidator(0)],
        verbose_name="Executed Amount",
    )
    unit = models.CharField(max_length=5, choices=UNIT_MAPPING)

    note = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, related_name="store")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")

    class Meta:
        verbose_name_plural = "inventories"

    def __str__(self):
        return self.name

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

    def increment_executed_amount(self, value):
        if value < 0:
            raise ValidationError("Increment value must be non-negative.")
        self.executed_amount += value
        self.save()

    def decrement_executed_amount(self, value):
        if value < 0:
            raise ValidationError("Decrement value must be non-negative.")
        if self.executed_amount - value < 0:
            raise ValidationError("Executed amount cannot be negative.")
        self.executed_amount -= value
        self.save()
