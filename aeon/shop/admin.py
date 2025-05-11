from django.contrib import admin

from .models import Category, Product, Rating, ImageSlider, ContactRequest, Brand, ProductImage, MenuItem, ProductAttribute, Attribute, AttributeValue
from django.utils.safestring import mark_safe

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1
    autocomplete_fields = ['attribute_value']

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    search_fields = ['value']
    autocomplete_fields = ['attribute']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'is_main', 'parent')

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
    
class ProductImageInLine(admin.StackedInline):
    model = ProductImage
    extra = 0
    fields = ('picture', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, instance):
        if instance.picture:
            return mark_safe(f'<img src="{instance.picture.url}" width="100" height="100" />')
        return 'Нет изображения'
    
    image_preview.short_description = 'Попередній перегляд'
    image_preview.allow_tags = True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'brand', 'slug', 'price', 'available', 'category', 'created_at', 'updated_at')
    fields = ('category', 'title', 'brand', 'color', 'slug', 'price', 'available', 'description')
    ordering = ('-created_at', '-updated_at')
    list_filter = ('available', 'created_at', 'updated_at')
    
    inlines = [ProductImageInLine, ProductAttributeInline]
    
    class Media:
        js = ('shop/js/product_image_preview.js',)

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
