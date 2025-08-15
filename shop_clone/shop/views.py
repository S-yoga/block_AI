
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register, Product

cart = []  # simple in-memory cart (not persistent)

def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if Register.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
        else:
            Register.objects.create(name=name, email=email, password=password)
            messages.success(request, "Registered successfully!")
            return redirect("login")
    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = Register.objects.filter(email=email, password=password).first()
        if user:
            request.session['user_id'] = user.id
            return redirect("shop")
        else:
            messages.error(request, "Invalid credentials!")
    return render(request, "login.html")

def shop_view(request):
    products = Product.objects.all()
    return render(request, "shop.html", {"products": products})

def add_to_cart(request, pid):
    product = Product.objects.get(id=pid)
    cart.append(product)
    messages.success(request, f"{product.name} added to cart!")
    return redirect("shop")

def view_cart(request):
    return render(request, "cart.html",{"cart":cart})

def remove_from_cart(request,pid):
    global cart
    cart = [ item for item in cart if item.id!=pid ]
    messages.success(request, "Item removed from cart!")
    return redirect("cart")
