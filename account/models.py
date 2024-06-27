from django.contrib.auth import get_user_model, models as auth_models
from django.core import validators
from django.db import models


class User(auth_models.AbstractUser):
    phone_number = models.CharField(
        null=False,
        blank=False,
        max_length=13,
        validators=[
            validators.RegexValidator(
                regex=r"^[0-9]{10,13}$",
                message="Please enter a phone number between 10 and 13 digits long, eg: 987654321.",
            )
        ],
    )
    additional_data = models.JSONField(null=True, blank=True, default=dict)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.phone_number

        super().save(*args, **kwargs)


class Address(models.Model):
    address = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "addresses"

    def __str__(self):
        return self.address
