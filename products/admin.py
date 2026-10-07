from django.contrib import admin
from django.utils.html import format_html
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'badge', 'is_best_seller', 'is_active', 'image_preview']
    list_filter = ['category', 'is_best_seller', 'is_active']
    search_fields = ['name', 'name_ar', 'category', 'description', 'ingredients']
    list_editable = ['price', 'is_best_seller', 'is_active']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'name_ar', 'category', 'category_ar', 'price', 'badge', 'badge_ar', 'is_best_seller', 'is_active')
        }),
        ('Media', {
            'fields': ('image', 'image_url')
        }),
        ('Descriptions & Details', {
            'fields': ('description', 'description_ar', 'how_to_use', 'how_to_use_ar', 'ingredients', 'ingredients_ar')
        }),
        ('Key Benefits', {
            'fields': ('benefits', 'benefits_ar'),
            'description': 'JSON array of strings, e.g. ["Lightweight", "Absorbs quickly"]'
        }),
    )

    def image_preview(self, obj):
        url = obj.effective_image_url
        if url:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', url)
        return "-"
    image_preview.short_description = 'Preview'
