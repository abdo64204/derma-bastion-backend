import base64
import re
from django.core.files.base import ContentFile
from django.utils import timezone
from rest_framework import serializers
from products.models import Product
from products.serializers import ProductSerializer
from .models import Order, OrderItem


class DeliveryDetailsSerializer(serializers.Serializer):
    fullName = serializers.CharField(min_length=3, max_length=150)
    phone = serializers.CharField()
    governorate = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    address = serializers.CharField(min_length=8)
    notes = serializers.CharField(required=False, allow_blank=True, default='')

    def validate_phone(self, value):
        cleaned = re.sub(r'\s+', '', value)
        if not re.match(r'^01[0125][0-9]{8}$', cleaned):
            raise serializers.ValidationError(
                "Must be a valid Egyptian mobile number (e.g. 01012345678, 011..., 012..., 015...)."
            )
        return cleaned


class OrderItemInputSerializer(serializers.Serializer):
    product = serializers.DictField()
    quantity = serializers.IntegerField(min_value=1)


class PaymentReceiptInputSerializer(serializers.Serializer):
    fileName = serializers.CharField(max_length=255, required=False, default='receipt.png')
    fileSize = serializers.IntegerField(required=False, default=0)
    fileType = serializers.CharField(max_length=100, required=False, default='image/png')
    dataUrl = serializers.CharField(required=False, allow_blank=True)


class PaymentInfoInputSerializer(serializers.Serializer):
    method = serializers.ChoiceField(choices=['cod', 'card', 'vodafone_cash', 'instapay'])
    status = serializers.ChoiceField(
        choices=['pending', 'verified', 'paid_on_delivery'],
        required=False,
        default='pending'
    )
    cardNetwork = serializers.CharField(required=False, allow_null=True)
    maskedCard = serializers.CharField(required=False, allow_null=True)
    gatewayNote = serializers.CharField(required=False, allow_null=True)
    receipt = PaymentReceiptInputSerializer(required=False, allow_null=True)


class OrderCreateSerializer(serializers.Serializer):
    delivery = DeliveryDetailsSerializer()
    items = serializers.ListField(child=OrderItemInputSerializer(), min_length=1)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    shipping = serializers.DecimalField(max_digits=10, decimal_places=2)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment = PaymentInfoInputSerializer()

    def create(self, validated_data):
        delivery_data = validated_data['delivery']
        items_data = validated_data['items']
        payment_data = validated_data['payment']

        # Determine payment status
        method = payment_data['method']
        default_status = 'paid_on_delivery' if method == 'cod' else 'pending'
        payment_status = payment_data.get('status') or default_status

        order = Order(
            full_name=delivery_data['fullName'],
            phone=delivery_data['phone'],
            governorate=delivery_data['governorate'],
            city=delivery_data['city'],
            address=delivery_data['address'],
            notes=delivery_data.get('notes', ''),
            subtotal=validated_data['subtotal'],
            shipping=validated_data['shipping'],
            total=validated_data['total'],
            payment_method=method,
            payment_status=payment_status,
            card_network=payment_data.get('cardNetwork'),
            masked_card=payment_data.get('maskedCard'),
            gateway_note=payment_data.get('gatewayNote'),
            status='placed',
        )

        # Handle receipt dataUrl if present
        receipt_data = payment_data.get('receipt')
        if receipt_data:
            order.receipt_file_name = receipt_data.get('fileName')
            order.receipt_file_size = receipt_data.get('fileSize')
            order.receipt_file_type = receipt_data.get('fileType')
            order.receipt_uploaded_at = timezone.now()

            data_url = receipt_data.get('dataUrl', '')
            if data_url and ';base64,' in data_url:
                header, b64data = data_url.split(';base64,', 1)
                file_content = base64.b64decode(b64data)
                ext = 'jpg' if 'jpeg' in header else ('png' if 'png' in header else 'webp')
                file_name = f"receipt_{order.id}.{ext}"
                order.receipt_image.save(file_name, ContentFile(file_content), save=False)

        order.save()

        # Create OrderItems
        for item_entry in items_data:
            prod_info = item_entry['product']
            prod_id = prod_info.get('id')
            product = None
            if prod_id:
                product = Product.objects.filter(id=prod_id).first()

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=prod_info.get('name', 'Product'),
                product_category=prod_info.get('category', ''),
                price=prod_info.get('price', 0.0),
                quantity=item_entry['quantity'],
                image_url=prod_info.get('image', '')
            )

        return order


class OrderItemDetailSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def get_product(self, obj):
        if obj.product:
            return ProductSerializer(obj.product, context=self.context).data
        return {
            'id': 0,
            'name': obj.product_name,
            'category': obj.product_category,
            'price': float(obj.price),
            'image': obj.image_url,
            'description': '',
            'benefits': [],
            'howToUse': '',
            'ingredients': '',
        }


class OrderDetailSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source='created_at', format='iso-8601', read_only=True)
    delivery = serializers.SerializerMethodField()
    items = OrderItemDetailSerializer(many=True, read_only=True)
    payment = serializers.SerializerMethodField()
    subtotal = serializers.FloatField()
    shipping = serializers.FloatField()
    total = serializers.FloatField()
    timeline = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'createdAt',
            'delivery',
            'items',
            'subtotal',
            'shipping',
            'total',
            'payment',
            'status',
            'timeline',
        ]

    def get_delivery(self, obj):
        return {
            'fullName': obj.full_name,
            'phone': obj.phone,
            'governorate': obj.governorate,
            'city': obj.city,
            'address': obj.address,
            'notes': obj.notes,
        }

    def get_payment(self, obj):
        request = self.context.get('request')
        receipt_url = None
        if obj.receipt_image:
            if request:
                receipt_url = request.build_absolute_uri(obj.receipt_image.url)
            else:
                receipt_url = obj.receipt_image.url

        receipt = None
        if obj.receipt_image or obj.receipt_file_name:
            receipt = {
                'fileName': obj.receipt_file_name or 'receipt.jpg',
                'fileSize': obj.receipt_file_size or 0,
                'fileType': obj.receipt_file_type or 'image/jpeg',
                'dataUrl': receipt_url,
                'uploadedAt': obj.receipt_uploaded_at.isoformat() if obj.receipt_uploaded_at else None
            }

        return {
            'method': obj.payment_method,
            'status': obj.payment_status,
            'cardNetwork': obj.card_network,
            'maskedCard': obj.masked_card,
            'receipt': receipt,
            'gatewayNote': obj.gateway_note,
        }

    def get_timeline(self, obj):
        return {
            'currentStepIndex': obj.get_current_step_index(),
            'status': obj.status,
            'placedAt': obj.created_at.isoformat() if obj.created_at else None,
            'confirmedAt': obj.confirmed_at.isoformat() if obj.confirmed_at else None,
            'shippedAt': obj.shipped_at.isoformat() if obj.shipped_at else None,
            'outForDeliveryAt': obj.out_for_delivery_at.isoformat() if obj.out_for_delivery_at else None,
            'deliveredAt': obj.delivered_at.isoformat() if obj.delivered_at else None,
        }
