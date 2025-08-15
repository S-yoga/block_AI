from django.db import models

class Register(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return self.name 