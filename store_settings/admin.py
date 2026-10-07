from django.contrib import admin
from .models import StoreSettings


@admin.register(StoreSettings)
class StoreSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Shipping Policy', {
            'fields': ('currency', 'free_shipping_from', 'shipping_fee'),
            'description': 'Shipping rules applied at checkout (Default: Free from 1500 EGP, otherwise 60 EGP)'
        }),
        ('Vodafone Cash Merchant Configuration', {
            'fields': ('vodafone_wallet_number', 'vodafone_merchant_name', 'vodafone_is_configured'),
            'description': 'Enter your registered 11-digit Vodafone Cash wallet number before launch.'
        }),
        ('InstaPay Business Configuration', {
            'fields': ('instapay_identifier', 'instapay_account_name', 'instapay_is_configured'),
            'description': 'Enter your InstaPay Payment Address (IPA, e.g. store@instapay) or IBAN.'
        }),
        ('Card Gateway (PSP Integration)', {
            'fields': ('card_provider_name', 'card_live_connected'),
            'description': 'Status of Egyptian payment gateway (Paymob, Fawry, Kashier).'
        }),
        ('Store Contact Information', {
            'fields': ('contact_phone', 'contact_whatsapp', 'contact_email', 'facebook_url', 'instagram_url', 'linkedin_url'),
            'description': 'Shown on Contact page and footer'
        }),
        ('Header Announcement Bar', {
            'fields': ('announcement_en', 'announcement_ar'),
        }),
    )

    def has_add_permission(self, request):
        # Disallow adding multiple settings instances
        if StoreSettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False
