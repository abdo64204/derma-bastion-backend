from django.db import models


class StoreSettings(models.Model):
    """
    Singleton model for dynamic store configurations, payment wallet numbers,
    shipping thresholds, and announcements.
    """
    # Shipping & Currency
    currency = models.CharField(max_length=10, default='EGP')
    free_shipping_from = models.DecimalField(max_digits=10, decimal_places=2, default=1500.00, help_text="Order subtotal threshold for free shipping (EGP)")
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=60.00, help_text="Standard shipping fee across Egypt (EGP)")

    # Vodafone Cash Configuration
    vodafone_wallet_number = models.CharField(max_length=20, blank=True, default='', help_text="Store's 11-digit Vodafone Cash wallet number")
    vodafone_merchant_name = models.CharField(max_length=100, default='Derma Bastion Official', help_text="Account name displayed to customers")
    vodafone_is_configured = models.BooleanField(default=False, help_text="Mark True once real wallet number is set")

    # InstaPay Configuration
    instapay_identifier = models.CharField(max_length=100, blank=True, default='', help_text="InstaPay Payment Address (IPA, e.g. dermabastion@instapay) or IBAN")
    instapay_account_name = models.CharField(max_length=100, blank=True, default='Derma Bastion Official')
    instapay_is_configured = models.BooleanField(default=False, help_text="Mark True once real InstaPay IPA is set")

    # Card Payment Gateway
    card_provider_name = models.CharField(max_length=50, default='Paymob', help_text="PSP Provider (Paymob, Fawry, Kashier)")
    card_live_connected = models.BooleanField(default=False, help_text="Whether live payment gateway processing is active")

    # Contact & Support Info
    contact_phone = models.CharField(max_length=30, default='+20 100 000 0000')
    contact_whatsapp = models.CharField(max_length=30, default='201000000000')
    contact_email = models.EmailField(default='hello@dermabastion.com')

    # Social links
    facebook_url = models.URLField(blank=True, default='https://facebook.com/')
    instagram_url = models.URLField(blank=True, default='https://instagram.com/')
    linkedin_url = models.URLField(blank=True, default='https://linkedin.com/')

    # Header announcement
    announcement_en = models.CharField(max_length=255, default='Free shipping on orders above {amount} {currency}')
    announcement_ar = models.CharField(max_length=255, default='شحن مجاني للطلبات فوق {amount} {currency}')

    class Meta:
        verbose_name = 'Store Configuration'
        verbose_name_plural = 'Store Configuration'

    def __str__(self):
        return "Derma Bastion Store Configuration"

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj
