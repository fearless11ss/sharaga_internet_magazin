from urllib.request import urlopen, Request
from urllib.error import URLError

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from products.models import Category, Product

# Только эти категории и товары относятся к AppleStore (без аксессуаров)
APPLE_CATEGORY_SLUGS = {'iphone', 'ipad', 'macbook'}
APPLE_PRODUCT_SLUGS = {
    'iphone-15-pro', 'iphone-15', 'ipad-pro-129',
    'macbook-air-m3', 'macbook-pro-14',
}

# Изображения товаров (Unsplash)
PRODUCT_IMAGES = {
    'iphone-15-pro': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=800&q=80',
    'iphone-15': 'https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=800&q=80',
    'ipad-pro-129': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&q=80',
    'macbook-air-m3': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&q=80',
    'macbook-pro-14': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&q=80',
}

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


def download_image(url, slug):
    """Скачивает изображение по URL и возвращает (filename, ContentFile) или None."""
    try:
        req = Request(url, headers={'User-Agent': USER_AGENT})
        resp = urlopen(req, timeout=15)
        data = resp.read()
        if len(data) < 1000:
            return None
        ext = '.jpg'
        content_type = resp.headers.get('Content-Type', '')
        if 'png' in content_type:
            ext = '.png'
        elif 'webp' in content_type:
            ext = '.webp'
        filename = f"{slug}{ext}"
        return filename, ContentFile(data)
    except (URLError, OSError) as e:
        return None


class Command(BaseCommand):
    help = 'Создание тестовых данных для магазина техники Apple'

    def handle(self, *args, **kwargs):
        # Удаляем товары не из тематики AppleStore (Samsung, футболки и т.п.)
        deleted_products = Product.objects.exclude(slug__in=APPLE_PRODUCT_SLUGS)
        count = deleted_products.count()
        deleted_products.delete()
        if count:
            self.stdout.write(self.style.WARNING(f'Удалено посторонних товаров: {count}'))

        # Удаляем старые категории не по тематике (Электроника, Одежда, Книги)
        Category.objects.exclude(slug__in=APPLE_CATEGORY_SLUGS).delete()

        categories_data = [
            {'name': 'iPhone', 'slug': 'iphone', 'description': 'Смартфоны iPhone'},
            {'name': 'iPad', 'slug': 'ipad', 'description': 'Планшеты iPad'},
            {'name': 'MacBook', 'slug': 'macbook', 'description': 'Ноутбуки MacBook'},
        ]
        for cat_data in categories_data:
            Category.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)

        products_data = [
            {
                'category': Category.objects.get(slug='iphone'),
                'name': 'iPhone 15 Pro',
                'slug': 'iphone-15-pro',
                'description': 'Титановый корпус, чип A17 Pro, камера 48 МП. Официальная гарантия.',
                'price': 119990.00,
                'stock': 25,
            },
            {
                'category': Category.objects.get(slug='iphone'),
                'name': 'iPhone 15',
                'slug': 'iphone-15',
                'description': 'Динамический остров, камера 48 МП, USB-C. Оригинальная техника Apple.',
                'price': 89990.00,
                'stock': 40,
            },
            {
                'category': Category.objects.get(slug='ipad'),
                'name': 'iPad Pro 12.9"',
                'slug': 'ipad-pro-129',
                'description': 'Чип M2, дисплей Liquid Retina XDR. Для творчества и работы.',
                'price': 129990.00,
                'stock': 15,
            },
            {
                'category': Category.objects.get(slug='macbook'),
                'name': 'MacBook Air M3',
                'slug': 'macbook-air-m3',
                'description': 'Чип M3, 13.6", до 18 часов работы. Тонкий и лёгкий.',
                'price': 119990.00,
                'stock': 20,
            },
            {
                'category': Category.objects.get(slug='macbook'),
                'name': 'MacBook Pro 14"',
                'slug': 'macbook-pro-14',
                'description': 'Чип M3 Pro, дисплей Liquid Retina XDR. Для профессионалов.',
                'price': 199990.00,
                'stock': 10,
            },
        ]

        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults=prod_data
            )
            # Загружаем или обновляем картинку по URL (для MagSafe/AirPods/iPad при смене URL — перезаписываем)
            if product.slug in PRODUCT_IMAGES:
                result = download_image(PRODUCT_IMAGES[product.slug], product.slug)
                if result:
                    filename, content = result
                    product.image.save(filename, content, save=True)
                    self.stdout.write(f'  → картинка: {product.name}')

        self.stdout.write(self.style.SUCCESS('Тестовые данные AppleStore созданы!'))
