from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product
from .models import Cart, CartItem
import json


def get_or_create_cart(request):
    """Получение или создание корзины."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def cart_view(request):
    """Отображение корзины."""
    cart = get_or_create_cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


@require_POST
def add_to_cart(request):
    """Добавление товара в корзину (AJAX или form)."""
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
    else:
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))

    if not product_id:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Не указан товар'}, status=400)
        return redirect('products:catalog')

    product = get_object_or_404(Product, id=product_id, available=True)
    cart = get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.total_items,
            'message': f'Товар "{product.name}" добавлен в корзину'
        })
    return redirect('cart')


@require_POST
def remove_from_cart(request, item_id):
    """Удаление товара из корзины."""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    return redirect('cart')
