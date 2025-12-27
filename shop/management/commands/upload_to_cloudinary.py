"""
Management command to upload existing media files to Cloudinary.
Run: python manage.py upload_to_cloudinary
"""
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from shop.models import Category, Product, ProductImage, Promotion, FlashSale


class Command(BaseCommand):
    help = 'Upload existing media files to Cloudinary and update database references'

    def handle(self, *args, **options):
        if not getattr(settings, 'USE_CLOUDINARY', False):
            self.stdout.write(self.style.ERROR('Cloudinary is not enabled. Set CLOUDINARY_URL environment variable.'))
            return

        self.stdout.write(self.style.SUCCESS('Starting Cloudinary upload...'))

        # Upload Category images
        categories = Category.objects.exclude(image='')
        self.stdout.write(f'Found {categories.count()} categories with images')
        for category in categories:
            if category.image and hasattr(category.image, 'file'):
                try:
                    # Save will trigger Cloudinary upload
                    category.save()
                    self.stdout.write(self.style.SUCCESS(f'✓ Uploaded: {category.image.name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'✗ Failed {category.image.name}: {e}'))

        # Upload Product main images
        products = Product.objects.exclude(main_image='')
        self.stdout.write(f'Found {products.count()} products with main images')
        for product in products:
            if product.main_image and hasattr(product.main_image, 'file'):
                try:
                    product.save()
                    self.stdout.write(self.style.SUCCESS(f'✓ Uploaded: {product.main_image.name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'✗ Failed {product.main_image.name}: {e}'))

        # Upload ProductImage images
        product_images = ProductImage.objects.exclude(image='')
        self.stdout.write(f'Found {product_images.count()} product gallery images')
        for img in product_images:
            if img.image and hasattr(img.image, 'file'):
                try:
                    img.save()
                    self.stdout.write(self.style.SUCCESS(f'✓ Uploaded: {img.image.name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'✗ Failed {img.image.name}: {e}'))

        # Upload Promotion images
        promotions = Promotion.objects.exclude(image='')
        self.stdout.write(f'Found {promotions.count()} promotions with images')
        for promo in promotions:
            if promo.image and hasattr(promo.image, 'file'):
                try:
                    promo.save()
                    self.stdout.write(self.style.SUCCESS(f'✓ Uploaded: {promo.image.name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'✗ Failed {promo.image.name}: {e}'))

        # Upload FlashSale images
        flash_sales = FlashSale.objects.exclude(image='')
        self.stdout.write(f'Found {flash_sales.count()} flash sales with images')
        for fs in flash_sales:
            if fs.image and hasattr(fs.image, 'file'):
                try:
                    fs.save()
                    self.stdout.write(self.style.SUCCESS(f'✓ Uploaded: {fs.image.name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'✗ Failed {fs.image.name}: {e}'))

        self.stdout.write(self.style.SUCCESS('\n✓ Upload complete!'))

