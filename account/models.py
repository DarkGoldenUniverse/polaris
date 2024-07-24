from django.contrib.auth import models as auth_models
from django.db import models


class User(auth_models.AbstractUser):
    additional_data = models.JSONField(null=True, blank=True, default=dict)

    def __str__(self):
        return self.username
