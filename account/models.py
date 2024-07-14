from django.contrib.auth import models as auth_models
from django.db import models


class User(auth_models.AbstractUser):
    additional_data = models.JSONField(null=True, blank=True, default=dict)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email

        super().save(*args, **kwargs)
