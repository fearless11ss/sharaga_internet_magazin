from django.shortcuts import render


def index(request):
    """Главная страница интернет-магазина AppleStore."""
    return render(request, 'shop/index.html')


def about(request):
    """Страница «О магазине»."""
    return render(request, 'shop/about.html')
