from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Register, Product, Category

# Register Page
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

# Login Page
def login_view(request):
    if request.session.get('user_id'):
        return redirect('shop')  # already logged in

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = Register.objects.filter(email=email, password=password).first()
        if user:
            request.session['user_id'] = user.id
            return redirect("shop")
        else:
            messages.error(request, "Invalid credentials!")
    return render(request,"login.html")
# Logout
def logout_view(request):
    request.session.flush()
    return redirect("login")

# Shop Page (Meesho clone)
def shop_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, "shop.html", {"products": products, "categories": categories})

# Category Filter
def category_view(request, cid):
    category = get_object_or_404(Category, id=cid)
    products = category.products.all()
    categories = Category.objects.all()
    return render(request, "shop.html", {"products": products, "categories": categories})

# Product Detail
def product_detail(request, pid):
    product = get_object_or_404(Product, id=pid)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    return render(request, "product_detail.html", {"product": product, "related": related_products})

# Add to Cart
def add_to_cart(request, pid):
    cart = request.session.get("cart", [])
    cart.append(pid)
    request.session["cart"] = list(set(cart))  # Remove duplicates
    messages.success(request, "Item added to cart!")
    return redirect("shop")

# View Cart
def view_cart(request):
    cart_ids = request.session.get("cart", [])
    products = Product.objects.filter(id__in=cart_ids)
    return render(request, "cart.html", {"cart_items": products})

# Remove from Cart
def remove_from_cart(request, pid):
    cart = request.session.get("cart", [])
    if pid in cart:
        cart.remove(pid)
        request.session["cart"] = cart
        messages.success(request, "Item removed from cart!")
    return redirect("cart")
