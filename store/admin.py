from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Cart, CartItem, Order, OrderItem, UserProfile

# Customize admin site
admin.site.site_header = "E-Store Administration"
admin.site.site_title = "E-Store Admin"
admin.site.index_title = "Welcome to E-Store Admin"

# Custom CSS for admin
class CustomAdminSite(admin.AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context['extra_css'] = '''
        <style>
        #header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            font-weight: bold !important;
            font-size: 18px !important;
            text-align: center !important;
            padding: 15px !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        }
        #header h1 {
            color: white !important;
            font-weight: bold !important;
            font-size: 24px !important;
            margin: 0 !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
        }
        .module h2 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            font-weight: bold !important;
            padding: 10px !important;
            border-radius: 5px !important;
        }
        </style>
        '''
        return context

# Use custom admin site
admin_site = CustomAdminSite(name='admin')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'created_at', 'image_preview']
    list_filter = ['created_at', 'stock']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock']
    readonly_fields = ['image_preview', 'created_at', 'updated_at']
    actions = ['delete_selected']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price', 'stock')
        }),
        ('Image Management', {
            'fields': ('image', 'image_preview'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px; object-fit: cover; border-radius: 8px; border: 2px solid #ddd;" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">No Image</span>')
    image_preview.short_description = 'Image Preview'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return self.readonly_fields
        else:  # Creating new object
            return ['image_preview', 'created_at', 'updated_at']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'total_price']
    list_filter = ['created_at']
    readonly_fields = ['created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username']
    list_editable = ['status']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'order_number', 'total_amount', 'status')
        }),
        ('Shipping Information', {
            'fields': ('shipping_address', 'phone_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order__status']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'profile_picture_preview']
    search_fields = ['user__username', 'phone_number']
    readonly_fields = ['profile_picture_preview']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'name', 'email', 'phone_number')
        }),
        ('Address', {
            'fields': ('address',)
        }),
        ('Profile Picture', {
            'fields': ('profile_picture', 'profile_picture_preview'),
            'classes': ('collapse',)
        }),
    )
    
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover; border-radius: 50%; border: 2px solid #ddd;" />',
                obj.profile_picture.url
            )
        return format_html('<span style="color: #999;">No Image</span>')
    profile_picture_preview.short_description = 'Profile Picture'
