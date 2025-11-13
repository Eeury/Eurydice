from django.contrib import admin

from .models import Category, Product, ProductImage, Promotion, FlashSale, FlashSaleItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "alt_text", "is_primary", "sort_order")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("title", "discount_percent", "start_at", "end_at", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


class FlashSaleItemInline(admin.TabularInline):
    model = FlashSaleItem
    extra = 1
    fields = ("product", "sale_price", "stock_limit")


@admin.register(FlashSale)
class FlashSaleAdmin(admin.ModelAdmin):
    list_display = ("title", "start_at", "end_at", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [FlashSaleItemInline]


