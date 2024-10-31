from django.contrib import admin

from .models import Category, Product, Rating, ImageSlider
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    ordering = ('name',)

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'slug', 'price', 'available', 'created_at', 'updated_at')
    ordering = ('title',)
    list_filter = ('available', 'created_at', 'updated_at')

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
