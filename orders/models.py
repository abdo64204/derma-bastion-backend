import random
from django.db import models
from django.utils import timezone
from products.models import Product


def generate_order_id():
    """Generates unique order ID in format DB-XXXXXX matching frontend convention"""
    while True:
        candidate = f"DB-{random.randint(100000, 999999)}"
        if not Order.objects.filter(id=candidate).exists():
            return candidate


EGYPT_GOVERNORATES = [
    ('Cairo', 'Cairo - القاهرة'),
    ('Giza', 'Giza - الجيزة'),
    ('Alexandria', 'Alexandria - الإسكندرية'),
    ('Qalyubia', 'Qalyubia - القليوبية'),
    ('Port Said', 'Port Said - بورسعيد'),
    ('Suez', 'Suez - السويس'),
    ('Damietta', 'Damietta - دمياط'),
    ('Dakahlia', 'Dakahlia - الدقهلية'),
    ('Sharqia', 'Sharqia - الشرقية'),
    ('Gharbia', 'Gharbia - الغربية'),
    ('Monufia', 'Monufia - المنوفية'),
    ('Kafr El Sheikh', 'Kafr El Sheikh - كفر الشيخ'),
    ('Beheira', 'Beheira - البحيرة'),
    ('Ismailia', 'Ismailia - الإسماعيلية'),
    ('Faiyum', 'Faiyum - الفيوم'),
    ('Beni Suef', 'Beni Suef - بني سويف'),
    ('Minya', 'Minya - المنيا'),
    ('Assiut', 'Assiut - أسيوط'),
    ('Sohag', 'Sohag - سوهاج'),
    ('Qena', 'Qena - قنا'),
    ('Luxor', 'Luxor - الأقصر'),
    ('Aswan', 'Aswan - أسوان'),
    ('Red Sea', 'Red Sea - البحر الأحمر'),
    ('New Valley', 'New Valley - الوادي الجديد'),
    ('Matrouh', 'Matrouh - مطروح'),
    ('North Sinai', 'North Sinai - شمال سيناء'),
    ('South Sinai', 'South Sinai - جنوب سيناء'),
]


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery (الدفع عند الاستلام)'),
        ('card', 'Credit / Debit Card (بطاقة بنكية)'),
        ('vodafone_cash', 'Vodafone Cash (فودافون كاش)'),
        ('instapay', 'InstaPay (انستاباي)'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending Review (قيد المراجعة)'),
        ('verified', 'Verified / Paid (تم الدفع والتحقق)'),
        ('paid_on_delivery', 'To be Paid on Delivery (دفع عند الاستلام)'),
        ('failed', 'Failed (فشل الدفع)'),
    ]

    ORDER_STATUS_CHOICES = [
        ('placed', 'Order Placed (تم استلام الطلب)'),
        ('confirmed', 'Confirmed (تم تأكيد الطلب)'),
        ('shipped', 'Shipped (تم الشحن)'),
        ('out_for_delivery', 'Out for Delivery (في الطريق للتسليم)'),
        ('delivered', 'Delivered (تم التوصيل بنجاح)'),
        ('cancelled', 'Cancelled (ملغي)'),
    ]

    # Primary key matching frontend 'DB-XXXXXX'
    id = models.CharField(primary_key=True, max_length=20, default=generate_order_id, editable=False)
    created_at = models.DateTimeField(default=timezone.now)

    # Delivery information
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    governorate = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    notes = models.TextField(blank=True, default='')

    # Financial details (in EGP)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    # Payment details
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='cod')
    payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS_CHOICES, default='pending')
    card_network = models.CharField(max_length=20, blank=True, null=True)
    masked_card = models.CharField(max_length=30, blank=True, null=True)
    gateway_note = models.CharField(max_length=255, blank=True, null=True)

    # Receipt uploaded for Vodafone Cash or InstaPay
    receipt_image = models.ImageField(upload_to='receipts/%Y/%m/', blank=True, null=True)
    receipt_file_name = models.CharField(max_length=255, blank=True, null=True)
    receipt_file_size = models.PositiveIntegerField(blank=True, null=True)
    receipt_file_type = models.CharField(max_length=50, blank=True, null=True)
    receipt_uploaded_at = models.DateTimeField(blank=True, null=True)

    # Fulfillment / Tracking Timeline
    status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, default='placed')
    confirmed_at = models.DateTimeField(blank=True, null=True)
    shipped_at = models.DateTimeField(blank=True, null=True)
    out_for_delivery_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order {self.id} - {self.full_name} ({self.total} EGP)"

    def get_current_step_index(self):
        status_map = {
            'placed': 0,
            'confirmed': 1,
            'shipped': 2,
            'out_for_delivery': 3,
            'delivered': 4,
            'cancelled': -1,
        }
        return status_map.get(self.status, 0)

    def advance_status(self):
        """Helper to move to next fulfillment status and set timestamp"""
        now = timezone.now()
        if self.status == 'placed':
            self.status = 'confirmed'
            self.confirmed_at = now
        elif self.status == 'confirmed':
            self.status = 'shipped'
            self.shipped_at = now
        elif self.status == 'shipped':
            self.status = 'out_for_delivery'
            self.out_for_delivery_at = now
        elif self.status == 'out_for_delivery':
            self.status = 'delivered'
            self.delivered_at = now
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, related_name='order_items')
    product_name = models.CharField(max_length=200)
    product_category = models.CharField(max_length=100, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    image_url = models.CharField(max_length=500, blank=True, default='')

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.quantity}x {self.product_name} ({self.price} EGP each)"

    @property
    def total_price(self):
        return self.price * self.quantity
