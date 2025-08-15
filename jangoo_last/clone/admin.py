from django.contrib import admin
from .models import Register, Product, Category

admin.site.register(Register)
admin.site.register(Product)
admin.site.register(Category)