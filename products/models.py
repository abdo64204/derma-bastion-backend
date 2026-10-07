from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Skin Care', 'Skin Care'),
        ('Hair Care', 'Hair Care'),
        ('Eye Care', 'Eye Care'),
    ]

    name = models.CharField(max_length=200, help_text="English product name")
    name_ar = models.CharField(max_length=200, blank=True, default='', help_text="Arabic product name")
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Skin Care')
    category_ar = models.CharField(max_length=100, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in EGP")
    
    # Image support: uploaded image or external URL
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, default='', help_text="Optional fallback image URL or asset path")
    
    badge = models.CharField(max_length=50, blank=True, default='', help_text="Badge text in English (e.g. Best Seller, New)")
    badge_ar = models.CharField(max_length=50, blank=True, default='', help_text="Badge text in Arabic")
    
    description = models.TextField(blank=True, default='', help_text="English description")
    description_ar = models.TextField(blank=True, default='', help_text="Arabic description")
    
    benefits = models.JSONField(default=list, blank=True, help_text="List of key benefits in English")
    benefits_ar = models.JSONField(default=list, blank=True, help_text="List of key benefits in Arabic")
    
    how_to_use = models.TextField(blank=True, default='', help_text="How to use instructions in English")
    how_to_use_ar = models.TextField(blank=True, default='', help_text="How to use instructions in Arabic")
    
    ingredients = models.TextField(blank=True, default='', help_text="Ingredients in English")
    ingredients_ar = models.TextField(blank=True, default='', help_text="Ingredients in Arabic")
    
    is_best_seller = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.name} ({self.price} EGP)"

    @property
    def effective_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url or ''
