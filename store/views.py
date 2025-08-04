from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
import uuid
from .models import Product, Cart, CartItem, Order, OrderItem, UserProfile
from django.contrib.auth.models import User

def home(request):
    """Home page with featured products"""
    products = Product.objects.filter(stock__gt=0).order_by('-created_at')[:8]
    return render(request, 'store/home.html', {'products': products})

def product_list(request):
    """Product listing with search and pagination"""
    products = Product.objects.filter(stock__gt=0)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'store/product_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })

def product_detail(request, product_id):
    """Individual product detail page"""
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(stock__gt=0).exclude(id=product_id)[:4]
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related_products
    })

def get_or_create_cart(request):
    """Helper function to get or create cart"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key, user=None)
    return cart

def add_to_cart(request, product_id):
    """Add product to cart"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > product.stock:
            messages.error(request, f'Only {product.stock} items available in stock.')
            return redirect('product_detail', product_id=product_id)
        
        cart = get_or_create_cart(request)
        
        # Check if item already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f'{product.name} added to cart!')
        return redirect('view_cart')
    
    return redirect('product_list')

def view_cart(request):
    """View shopping cart"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    total = sum(item.total_price for item in cart_items)
    
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def update_cart_item(request, item_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        elif quantity > cart_item.product.stock:
            messages.error(request, f'Only {cart_item.product.stock} items available.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully.')
    
    return redirect('view_cart')

def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')

@login_required
def checkout(request):
    """Checkout process"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.error(request, 'Your cart is empty.')
        return redirect('product_list')
    
    total = sum(item.total_price for item in cart_items)
    
    if request.method == 'POST':
        # Get form data
        shipping_address = request.POST.get('shipping_address')
        phone_number = request.POST.get('phone_number')
        
        if not shipping_address or not phone_number:
            messages.error(request, 'Please fill all required fields.')
            return render(request, 'store/checkout.html', {
                'cart_items': cart_items,
                'total': total
            })
        
        try:
            with transaction.atomic():
                # Create order
                order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
                order = Order.objects.create(
                    user=request.user,
                    order_number=order_number,
                    total_amount=total,
                    shipping_address=shipping_address,
                    phone_number=phone_number
                )
                
                # Create order items
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )
                    
                    # Update stock
                    cart_item.product.stock -= cart_item.quantity
                    cart_item.product.save()
                
                # Clear cart
                cart.delete()
                
                messages.success(request, f'Order placed successfully! Order number: {order_number}')
                return redirect('order_confirmation', order_id=order.id)
                
        except Exception as e:
            messages.error(request, 'An error occurred while processing your order.')
    
    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_confirmation.html', {'order': order})

@login_required
def order_history(request):
    """User's order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    """Order detail page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})

def register(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'store/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'store/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'store/register.html')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')
    
    return render(request, 'store/register.html')

def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'store/login.html')

@login_required
def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile(request):
    """User profile page"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update profile
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        profile.phone_number = request.POST.get('phone_number', '')
        profile.address = request.POST.get('address', '')
        
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'store/profile.html', {'profile': profile})
