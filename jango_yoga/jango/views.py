from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Register, Product, Category

# REGISTER
def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if Register.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists! Please login.")
            return redirect("login")
        else:
            Register.objects.create(name=name, email=email, password=password)
            messages.success(request, "Registered successfully! Please login.")
            return redirect("login")
    return render(request, "register.html")

# LOGIN
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = Register.objects.filter(email=email, password=password).first()
        if user:
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            return redirect("shop")
        else:
            messages.error(request, "Invalid credentials!")
    return render(request, "login.html")

# LOGOUT
def logout_view(request):
    request.session.flush()
    return redirect("login")

# SHOP PAGE
def shop_view(request):
    if 'user_id' not in request.session:
        return redirect("login")
    search = request.GET.get("search", "")
    products = Product.objects.filter(name__icontains=search) if search else Product.objects.all()
    categories = Category.objects.all()
    return render(request, "shop.html", {"products": products, "categories": categories})

# CATEGORY FILTER
def category_view(request, cid):
    if 'user_id' not in request.session:
        return redirect("login")
    category = get_object_or_404(Category, id=cid)
    products = category.products.all()
    categories = Category.objects.all()
    return render(request, "shop.html", {"products": products, "categories": categories})

# PRODUCT DETAIL
def product_detail(request, pid):
    if 'user_id' not in request.session:
        return redirect("login")
    product = get_object_or_404(Product, id=pid)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    return render(request, "product_detail.html", {"product": product, "related": related_products})

# ADD TO CART
def add_to_cart(request, pid):
    if 'user_id' not in request.session:
        return redirect("login")
    cart = request.session.get("cart", [])
    if pid not in cart:
        cart.append(pid)
    request.session["cart"] = cart
    messages.success(request, "Item added to cart!")
    return redirect("shop")

# VIEW CART
def view_cart(request):
    if 'user_id' not in request.session:
        return redirect("login")
    cart_ids = request.session.get("cart", [])
    products = Product.objects.filter(id__in=cart_ids)
    return render(request, "cart.html", {"cart_items": products})

# REMOVE FROM CART
def remove_from_cart(request, pid):
    cart = request.session.get("cart", [])
    if pid in cart:
        cart.remove(pid)
    request.session["cart"] = cart
    messages.success(request, "Item removed from cart!")
    return redirect("cart")
# CATEGORY PAGE (Separate Page)
def category_view(request, cid):
    if 'user_id' not in request.session:
        return redirect("login")
    category = get_object_or_404(Category, id=cid)
    products = category.products.all()
    categories = Category.objects.all()
    return render(request, "category_page.html", {
        "category": category,
        "products": products,
        "categories": categories})
