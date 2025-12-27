"""
Script to upload all media files to Cloudinary.
Run: python upload_media_to_cloudinary.py

This script will:
1. Find all media files in the media/ directory
2. Upload them to Cloudinary
3. Update the database records with Cloudinary URLs
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Eurydice.settings')
django.setup()

from django.conf import settings
import cloudinary
import cloudinary.uploader
from shop.models import Category, Product, ProductImage, Promotion, FlashSale


def upload_file_to_cloudinary(file_path, folder=None):
    """Upload a file to Cloudinary and return the public_id"""
    try:
        upload_result = cloudinary.uploader.upload(
            file_path,
            folder=folder,
            resource_type="image"
        )
        return upload_result['public_id'], upload_result['secure_url']
    except Exception as e:
        print(f"Error uploading {file_path}: {e}")
        return None, None


def main():
    if not getattr(settings, 'USE_CLOUDINARY', False):
        print("ERROR: Cloudinary is not enabled. Set CLOUDINARY_URL environment variable.")
        return

    media_root = BASE_DIR / "media"
    if not media_root.exists():
        print(f"Media directory not found: {media_root}")
        return

    print("Starting Cloudinary upload...\n")

    # Upload Category images
    categories = Category.objects.exclude(image='')
    print(f"Processing {categories.count()} category images...")
    for category in categories:
        if category.image:
            file_path = media_root / category.image.name
            if file_path.exists():
                public_id, url = upload_file_to_cloudinary(file_path, folder="categories")
                if public_id:
                    category.image.name = public_id
                    category.save()
                    print(f"✓ Uploaded: {category.image.name}")
            else:
                print(f"⚠ File not found: {file_path}")

    # Upload Product main images
    products = Product.objects.exclude(main_image='')
    print(f"\nProcessing {products.count()} product main images...")
    for product in products:
        if product.main_image:
            file_path = media_root / product.main_image.name
            if file_path.exists():
                public_id, url = upload_file_to_cloudinary(file_path, folder="products/main")
                if public_id:
                    product.main_image.name = public_id
                    product.save()
                    print(f"✓ Uploaded: {product.main_image.name}")
            else:
                print(f"⚠ File not found: {file_path}")

    # Upload ProductImage gallery images
    product_images = ProductImage.objects.exclude(image='')
    print(f"\nProcessing {product_images.count()} product gallery images...")
    for img in product_images:
        if img.image:
            file_path = media_root / img.image.name
            if file_path.exists():
                public_id, url = upload_file_to_cloudinary(file_path, folder="products/gallery")
                if public_id:
                    img.image.name = public_id
                    img.save()
                    print(f"✓ Uploaded: {img.image.name}")
            else:
                print(f"⚠ File not found: {file_path}")

    # Upload Promotion images
    promotions = Promotion.objects.exclude(image='')
    print(f"\nProcessing {promotions.count()} promotion images...")
    for promo in promotions:
        if promo.image:
            file_path = media_root / promo.image.name
            if file_path.exists():
                public_id, url = upload_file_to_cloudinary(file_path, folder="promotions")
                if public_id:
                    promo.image.name = public_id
                    promo.save()
                    print(f"✓ Uploaded: {promo.image.name}")
            else:
                print(f"⚠ File not found: {file_path}")

    # Upload FlashSale images
    flash_sales = FlashSale.objects.exclude(image='')
    print(f"\nProcessing {flash_sales.count()} flash sale images...")
    for fs in flash_sales:
        if fs.image:
            file_path = media_root / fs.image.name
            if file_path.exists():
                public_id, url = upload_file_to_cloudinary(file_path, folder="flash_sales")
                if public_id:
                    fs.image.name = public_id
                    fs.save()
                    print(f"✓ Uploaded: {fs.image.name}")
            else:
                print(f"⚠ File not found: {file_path}")

    print("\n✓ Upload complete!")


if __name__ == "__main__":
    main()

