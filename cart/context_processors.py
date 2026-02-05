from .views import get_or_create_cart


def cart_context(request):
    """Добавляет корзину во все шаблоны."""
    cart = None
    try:
        cart = get_or_create_cart(request)
    except Exception:
        pass
    return {'cart': cart}
