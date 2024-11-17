from django.contrib import admin

from .models import Category, Product, Rating, ImageSlider, ContactRequest, Brand
from django.utils.safestring import mark_safe

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    ordering = ('name',)

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'slug', 'price', 'available', 'created_at', 'updated_at')
    fields = ('title', 'brand', 'color', 'slug', 'price', 'image', 'image_preview', 'available',)
    readonly_fields = ('image_preview',)
    ordering = ('-created_at', '-updated_at')
    list_filter = ('available', 'created_at', 'updated_at')

    class Media:
        js = ('shop/js/product_image_preview.js',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="200" style="margin-top: 10px;" />')
        return "No image available"

    image_preview.short_description = "Поточне зображення"

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}
    
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating')
    ordering = ('product',)
    list_filter = ('rating', 'product')

@admin.register(ImageSlider)
class ImageSliderAdmin(admin.ModelAdmin):
    list_display = ('product', 'created_at')
    ordering = ('created_at',)
    list_filter = ('created_at',)

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info', 'subject', 'message', 'created_at',)
    ordering = ('created_at',)
    list_filter = ('subject',)
