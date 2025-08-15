
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Register, Product, CartItem,ProductImage

# Helper: get current logged-in user id from session

def get_session_user_id(request):
    return request.session.get('user_id')

# Home / Product List with Search

def home(request):
    q = request.GET.get('q')
    if q:
        products = Product.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )
        if not products.exists():
            messages.info(request, 'No products found')
    else:
        products = Product.objects.all()

    return render(request, 'home.html', {
        'products': products,
        'user_name': request.session.get('user_name')
    })

# Register

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not name or not email or not password:
            messages.error(request, 'All fields are required')
            return redirect('register')

        # prevent duplicates
        if Register.objects.filter(Q(name=name) | Q(email=email)).exists():
            messages.error(request, 'User already exists. Try a different name/email.')
            return redirect('register')

        user = Register.objects.create(name=name, email=email, password=password)
        messages.success(request, 'Registered successfully. Please login.')
        return redirect('login')

    return render(request, 'register.html')

# Login

def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        user = Register.objects.filter(name=name, password=password).first()
        if user is None:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

        request.session['user_id'] = user.id
        request.session['user_name'] = user.name
        messages.success(request, f'Welcome {user.name}')
        return redirect('home')

    return render(request, 'login.html')

# Logout

def logout_view(request):
    request.session.flush()
    messages.info(request, 'Logged out')
    return redirect('home')

# Add to cart (requires login)

def add_to_cart(request, product_id):
    user_id = get_session_user_id(request)
    if not user_id:
        messages.error(request, 'Please login first')
        return redirect('login')

    # simple get without get_object_or_404
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, 'Product not found')
        return redirect('home')

    item = CartItem.objects.filter(user_id=user_id, product=product).first()
    if item:
        item.quantity += 1
        item.save()
    else:
        CartItem.objects.create(user_id=user_id, product=product, quantity=1)

    messages.success(request, f'Added {product.name} to cart')
    return redirect('home')


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, 'Product not found')
        return redirect('home')

    # Extra images of this product
    extra_images = ProductImage.objects.filter(product=product)

    # Other products to suggest (exclude current product)
    related_products = Product.objects.exclude(id=product.id)[:6]  # limit to 6

    return render(request, 'product_detail.html', {
        'product': product,
        'extra_images': extra_images,
        'related_products': related_products})


# View cart (simple list, no table)
def view_cart(request):
    user_id = get_session_user_id(request)
    if not user_id:
        messages.error(request, 'Please login to view cart')
        return redirect('login')

    items = CartItem.objects.filter(user_id=user_id).select_related('product')
    total = sum([i.subtotal() for i in items])
    return render(request, 'cart_simple.html', {'items': items, 'total':total})


# Remove single cart item

def remove_from_cart(request, item_id):
    user_id = get_session_user_id(request)
    if not user_id:
        return redirect('login')

    item = CartItem.objects.filter(id=item_id, user_id=user_id).first()
    if item:
        item.delete()
        messages.info(request, 'Item removed')
    else:
        messages.error(request, 'Item not found')
    return redirect('cart')
