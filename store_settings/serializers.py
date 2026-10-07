from rest_framework import serializers
from .models import StoreSettings


class StoreSettingsSerializer(serializers.ModelSerializer):
    vodafoneCash = serializers.SerializerMethodField()
    instapay = serializers.SerializerMethodField()
    cardGateway = serializers.SerializerMethodField()
    shipping = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()
    announcement = serializers.SerializerMethodField()

    class Meta:
        model = StoreSettings
        fields = [
            'currency',
            'vodafoneCash',
            'instapay',
            'cardGateway',
            'shipping',
            'contact',
            'announcement',
        ]

    def get_vodafoneCash(self, obj):
        return {
            'walletNumber': obj.vodafone_wallet_number,
            'merchantName': obj.vodafone_merchant_name,
            'isConfigured': bool(obj.vodafone_wallet_number and obj.vodafone_is_configured),
        }

    def get_instapay(self, obj):
        return {
            'identifier': obj.instapay_identifier,
            'accountName': obj.instapay_account_name,
            'isConfigured': bool(obj.instapay_identifier and obj.instapay_is_configured),
        }

    def get_cardGateway(self, obj):
        return {
            'providerName': obj.card_provider_name,
            'isLiveGatewayConnected': obj.card_live_connected,
            'integrationGuide': (
                'To enable live card processing (Visa, Mastercard, Meeza), connect an Egyptian payment gateway '
                '(e.g., Paymob Accept, Fawry Pay, or Kashier).'
            )
        }

    def get_shipping(self, obj):
        return {
            'freeShippingFrom': float(obj.free_shipping_from),
            'shippingFee': float(obj.shipping_fee),
            'currency': obj.currency,
        }

    def get_contact(self, obj):
        return {
            'phone': obj.contact_phone,
            'whatsappNumber': obj.contact_whatsapp,
            'email': obj.contact_email,
            'facebookUrl': obj.facebook_url,
            'instagramUrl': obj.instagram_url,
            'linkedinUrl': obj.linkedin_url,
        }

    def get_announcement(self, obj):
        return {
            'en': obj.announcement_en,
            'ar': obj.announcement_ar,
        }
