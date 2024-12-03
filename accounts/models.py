from django.contrib.auth.models import AbstractUser
from django.db import models


class Worker(AbstractUser):
    class Role(models.TextChoices):
        CLEANER = "cleaner", "Cleaner"
        AUDITOR = "auditor", "Auditor"

    role = models.CharField(max_length=8, choices=Role.choices)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"

