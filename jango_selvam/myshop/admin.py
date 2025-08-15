
from django.contrib import admin
from .models import Register, Product, CartItem

admin.site.register(Register)
admin.site.register(Product)
admin.site.register(CartItem)