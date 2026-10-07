from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_category', 'price', 'quantity', 'total_price']
    can_delete = False

    def total_price(self, obj):
        return f"{obj.total_price} EGP"
    total_price.short_description = 'Line Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'full_name',
        'phone',
        'governorate',
        'total_egp',
        'payment_method_badge',
        'payment_status_badge',
        'receipt_thumbnail',
        'status_badge',
        'created_at_formatted'
    ]
    list_filter = ['status', 'payment_status', 'payment_method', 'governorate', 'created_at']
    search_fields = ['id', 'full_name', 'phone', 'city', 'address', 'notes']
    readonly_fields = [
        'id',
        'created_at',
        'subtotal',
        'shipping',
        'total',
        'receipt_preview_large',
        'receipt_file_name',
        'receipt_file_size',
        'receipt_uploaded_at',
        'confirmed_at',
        'shipped_at',
        'out_for_delivery_at',
        'delivered_at',
        'updated_at'
    ]
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order & Customer Overview', {
            'fields': ('id', 'status', 'created_at', 'full_name', 'phone')
        }),
        ('Delivery Address (Egypt)', {
            'fields': ('governorate', 'city', 'address', 'notes')
        }),
        ('Payment Information', {
            'fields': (
                'payment_method',
                'payment_status',
                'card_network',
                'masked_card',
                'gateway_note',
                'receipt_preview_large',
                'receipt_file_name',
                'receipt_file_size',
                'receipt_uploaded_at'
            )
        }),
        ('Financials', {
            'fields': ('subtotal', 'shipping', 'total')
        }),
        ('Tracking & Fulfillment Timestamps', {
            'fields': (
                'confirmed_at',
                'shipped_at',
                'out_for_delivery_at',
                'delivered_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )

    actions = [
        'mark_payment_verified',
        'mark_status_confirmed',
        'mark_status_shipped',
        'mark_status_out_for_delivery',
        'mark_status_delivered',
    ]

    def total_egp(self, obj):
        return f"{obj.total} EGP"
    total_egp.short_description = 'Total'

    def created_at_formatted(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at_formatted.short_description = 'Date Placed'

    def payment_method_badge(self, obj):
        method_labels = {
            'cod': ('#555', 'Cash on Delivery'),
            'card': ('#1e40af', 'Credit/Debit Card'),
            'vodafone_cash': ('#b91c1c', 'Vodafone Cash'),
            'instapay': ('#6d28d9', 'InstaPay'),
        }
        color, label = method_labels.get(obj.payment_method, ('#333', obj.payment_method))
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 8px; border-radius:12px; font-size:11px; font-weight:600;">{}</span>',
            color, label
        )
    payment_method_badge.short_description = 'Payment'

    def payment_status_badge(self, obj):
        status_colors = {
            'pending': ('#d97706', 'Pending'),
            'verified': ('#15803d', 'Verified'),
            'paid_on_delivery': ('#0284c7', 'Pay on Delivery'),
            'failed': ('#dc2626', 'Failed'),
        }
        color, label = status_colors.get(obj.payment_status, ('#666', obj.payment_status))
        return format_html(
            '<span style="border:1px solid {}; color:{}; padding:2px 7px; border-radius:10px; font-size:11px; font-weight:600;">{}</span>',
            color, color, label
        )
    payment_status_badge.short_description = 'Pay Status'

    def status_badge(self, obj):
        order_colors = {
            'placed': ('#64748b', 'Placed'),
            'confirmed': ('#0284c7', 'Confirmed'),
            'shipped': ('#7c3aed', 'Shipped'),
            'out_for_delivery': ('#ea580c', 'Out for Delivery'),
            'delivered': ('#16a34a', 'Delivered'),
            'cancelled': ('#dc2626', 'Cancelled'),
        }
        color, label = order_colors.get(obj.status, ('#333', obj.status))
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 8px; border-radius:4px; font-size:11px; font-weight:600;">{}</span>',
            color, label
        )
    status_badge.short_description = 'Fulfillment'

    def receipt_thumbnail(self, obj):
        if obj.receipt_image:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="width:40px; height:40px; object-fit:cover; border-radius:4px; border:1px solid #ccc;" />'
                '</a>',
                obj.receipt_image.url, obj.receipt_image.url
            )
        return "-"
    receipt_thumbnail.short_description = 'Receipt'

    def receipt_preview_large(self, obj):
        if obj.receipt_image:
            return format_html(
                '<div style="margin-top:5px;">'
                '<a href="{}" target="_blank" style="display:inline-block; margin-bottom:8px; font-weight:bold; color:#2563eb;">🔍 Open Full Image in New Tab</a><br>'
                '<img src="{}" style="max-width:400px; max-height:400px; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.15);" />'
                '</div>',
                obj.receipt_image.url, obj.receipt_image.url
            )
        return "No receipt uploaded for this order."
    receipt_preview_large.short_description = 'Receipt Preview'

    # Admin actions
    def mark_payment_verified(self, request, queryset):
        count = queryset.update(payment_status='verified')
        self.message_user(request, f"{count} orders marked as payment VERIFIED.")
    mark_payment_verified.short_description = "Verify payment for selected orders"

    def mark_status_confirmed(self, request, queryset):
        now = timezone.now()
        count = queryset.update(status='confirmed', confirmed_at=now)
        self.message_user(request, f"{count} orders updated to CONFIRMED.")
    mark_status_confirmed.short_description = "Set fulfillment status: Confirmed"

    def mark_status_shipped(self, request, queryset):
        now = timezone.now()
        count = queryset.update(status='shipped', shipped_at=now)
        self.message_user(request, f"{count} orders updated to SHIPPED.")
    mark_status_shipped.short_description = "Set fulfillment status: Shipped"

    def mark_status_out_for_delivery(self, request, queryset):
        now = timezone.now()
        count = queryset.update(status='out_for_delivery', out_for_delivery_at=now)
        self.message_user(request, f"{count} orders updated to OUT FOR DELIVERY.")
    mark_status_out_for_delivery.short_description = "Set fulfillment status: Out for Delivery"

    def mark_status_delivered(self, request, queryset):
        now = timezone.now()
        count = queryset.update(status='delivered', delivered_at=now)
        self.message_user(request, f"{count} orders updated to DELIVERED.")
    mark_status_delivered.short_description = "Set fulfillment status: Delivered"
