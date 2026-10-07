from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'created_at', 'is_read', 'is_replied']
    list_filter = ['is_read', 'is_replied', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message']
    list_editable = ['is_read', 'is_replied']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Message Info', {
            'fields': ('name', 'email', 'phone', 'subject', 'message', 'created_at')
        }),
        ('Status & Response Notes', {
            'fields': ('is_read', 'is_replied', 'admin_notes')
        }),
    )
