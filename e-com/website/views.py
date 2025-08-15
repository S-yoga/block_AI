from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from django.db.models import Q
from .models import Register

# Hardcoded product list
PRODUCTS = [
    {"id":1,"category":"laptop", "name": "Laptop Pro 14", "description": "High performance laptop with 16GB RAM and 512GB SSD.", "price": 85000, "rating": 4.7, "image": "images/laptop.jpg"},
     {"id":2,"category":"laptop", "name": "Laptop Pro 15", "description": "High performance laptop with 16GB RAM and 512GB SSD.", "price": 85000, "rating": 4.7, "image": "images/laptop.jpg"},
    { "id":3,"category":"laptop","name": "Laptop Pro 16", "description": "High performance laptop with 16GB RAM and 512GB SSD.", "price": 85000, "rating": 4.7, "image": "images/laptop.jpg"},
    { "id":4,"category":"laptop","name": "Laptop Pro 17", "description": "High performance laptop with 16GB RAM and 512GB SSD.", "price": 85000, "rating": 4.7, "image": "images/laptop.jpg"},
     { "id":5,"category":"laptop","name": "Laptop Pro 18", "description": "High performance laptop with 16GB RAM and 512GB SSD.", "price": 85000, "rating": 4.7, "image": "images/laptop.jpg"},
    { "id":6,"category":"laptop","name": "Laptop Pro 19", "description": "High performance laptop with 16GB RAM and 512GB SSD.", "price": 85000, "rating": 4.7, "image": "images/laptop.jpg"},

    {"id":7,"category":"mobiles","name": "SuperPhone X", "description": "Latest smartphone with excellent camera and battery life.", "price": 32000, "rating": 4.5, "image": "images/mobile_sam.webp"},
    {"id":8,"category":"mobiles","name": "SuperPhone X", "description": "Latest smartphone with excellent camera and battery life.", "price": 32000, "rating": 4.5, "image":"images/mobile_sam.webp" },
    {"id":9,"category":"mobiles","name": "SuperPhone X", "description": "Latest smartphone with excellent camera and battery life.", "price": 32000, "rating": 4.5, "image": "images/mobile_sam.webp"},
    {"id":10,"category":"mobiles","name": "SuperPhone X", "description": "Latest smartphone with excellent camera and battery life.", "price": 32000, "rating": 4.5, "image": "images/mobile_sam.webp"},
    {"id":11,"category":"mobiles","name": "SuperPhone X", "description": "Latest smartphone with excellent camera and battery life.", "price": 32000, "rating": 4.5, "image": "images/mobile_sam.webp"},

    {"id":12,"category":"watches" , "name": "Smart Watch Z", "description": "Fitness-focused smartwatch with heart-rate monitor.", "price": 7000, "rating": 4.2, "image": "images/watch.jpg"},
    {"id":13,"category":"watches" , "name": "Smart Watch Z", "description": "Fitness-focused smartwatch with heart-rate monitor.", "price": 7000, "rating": 4.2, "image": "images/watch.jpg"},
    {"id":14,"category":"watches" , "name": "Smart Watch Z", "description": "Fitness-focused smartwatch with heart-rate monitor.", "price": 7000, "rating": 4.2, "image": "images/watch.jpg"},
    {"id":15,"category":"watches" , "name": "Smart Watch Z", "description": "Fitness-focused smartwatch with heart-rate monitor.", "price": 7000, "rating": 4.2, "image": "images/watch.jpg"},
    {"id":16,"category":"watches" , "name": "Smart Watch Z", "description": "Fitness-focused smartwatch with heart-rate monitor.", "price": 7000, "rating": 4.2, "image": "images/watch.jpg"},

    {"id":17,"category":"Headphones", "name": "NoiseBeats Headphones", "description": "Over-ear noise-cancelling headphones with deep bass.", "price": 4500, "rating": 4.4, "image": "images/head_phone.jpg"},
    { "id":18,"category":"Headphones","name": "NoiseBeats Headphones", "description": "Over-ear noise-cancelling headphones with deep bass.", "price": 4500, "rating": 4.4, "image": "images/head_phone.jpg"},
    { "id":19,"category":"Headphones","name": "NoiseBeats Headphones", "description": "Over-ear noise-cancelling headphones with deep bass.", "price": 4500, "rating": 4.4, "image": "images/head_phone.jpg"},
    { "id":20,"category":"Headphones","name": "NoiseBeats Headphones", "description": "Over-ear noise-cancelling headphones with deep bass.", "price": 4500, "rating": 4.4, "image":"images/head_phone.jpg"},
    { "id":21,"category":"Headphones","name": "NoiseBeats Headphones", "description": "Over-ear noise-cancelling headphones with deep bass.", "price": 4500, "rating": 4.4, "image": "images/head_phone.jpg"},

]

def register_view(request):

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        mobile = request.POST.get("mobile", "").strip()
        password = request.POST.get("password", "").strip()

        # if not name or not password or (not email and not mobile):
        #     messages.error(request, "Please provide name, password, and email or mobile.")
        #     return redirect("register")
        if email and Register.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register_url")
        if mobile and Register.objects.filter(mobile=mobile).exists():
            messages.error(request, "Mobile already registered.")
            return redirect("register_url")
        register_info={
            'name':name,
            'email':email,
            'mobile':mobile,
            'password':password,
        }
        Register.objects.create(**register_info)
        messages.success(request, "Registered successfully. Please login.")
        return redirect("login")
    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("email_or_mobile", "").strip()
        password = request.POST.get("password", "").strip()
        # if not identifier or not password:
        #     messages.error(request, "Enter both fields.")
        #     return redirect("login")
        user = Register.objects.filter(Q(email__iexact=identifier) | Q(mobile__iexact=identifier),password=password ).first()
        if user:
            request.session["user_id"] = user.id
            request.session["user_name"] = user.name
            # if "cart" not in request.session:
            #     request.session["cart"] = []
            return redirect("shop")
        else:
            messages.error(request, "Invalid credentials.")
            return redirect("login")
    return render(request,"login.html")


def shop_view(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip().lower()

    products = PRODUCTS

    # Filter by category
    if category:
        products = [p for p in products if p["category"].lower() == category]

    # Filter by search
    if query:
        products = [p for p in products if query.lower() in p["name"].lower()]

    return render(request, "shop.html", {
        "products": products,
        "selected_category":category})
    
    # query = request.GET.get("q", "").strip()
    # products = PRODUCTS
    # if query:
    #     products = [p for p in PRODUCTS if query.lower() in p["name"].lower()]
    # return render(request, "shop.html", {"products": products})

def add_to_cart(request, pid):
    cart = request.session.get("cart", [])
    if pid not in cart:
        cart.append(pid)
    request.session["cart"] = cart
    messages.success(request, "Item added to cart.")
    return redirect("shop")

def view_cart(request):
    cart = request.session.get("cart", [])
    #cart_items=list(reversed(cart))
    cart_items = [p for p in PRODUCTS if p["id"] in cart]
    return render(request, "cart.html", {"cart_items": cart_items})

def remove_from_cart(request, pid):
    cart = request.session.get("cart", [])
    if pid in cart:
        cart.remove(pid)
    request.session["cart"] = cart
    messages.success(request, "Item removed from cart.")
    return redirect("view_cart")

def logout_view(request):
    request.session.flush()
    messages.success(request,"logged out successfully.")
    return redirect("login")