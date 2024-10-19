from django.shortcuts import redirect, render, get_object_or_404
from .models import Cart, CartItem, Product
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1

    cart_item.save()
    messages.success(request, f'Added {product.name} to your cart.')
    return redirect('cart')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    print(f"Cart ID: {cart.id}, Items: {list(items)}")

    return render(request, 'store/cart.html', {'cart': cart, 'items': items})

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart.items.all())

    context = {
        'cart_items': cart.items.all(),
        'total_price': total_price,
    }
    return render(request, 'store/checkout.html', context)

@login_required
def update_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        item.quantity = quantity
        item.save()
        messages.success(request, f'Updated {item.product.name} quantity to {quantity}.')

    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')

@require_POST
@login_required
def process_checkout(request):
    full_name = request.POST.get('full_name')
    address = request.POST.get('address')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip_code = request.POST.get('zip')
    country = request.POST.get('country')
    card_number = request.POST.get('card_number')
    expiry_date = request.POST.get('expiry_date')
    cvv = request.POST.get('cvv')

    # Clear the cart after processing
    Cart.objects.filter(user=request.user).delete()
    messages.success(request, 'Your order has been placed successfully!')
    return redirect('home')
