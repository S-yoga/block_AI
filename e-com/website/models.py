from django.db import models


class Register(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True, unique=True)
    mobile = models.CharField(max_length=20, blank=True, null=True, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name} ({self.email or self.mobile})"
