# store/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import UserAccount, Brand, Product, ShoppingCart, CustomerOrder, OrderItem


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "phone_number", "is_superuser")
    list_filter = ("is_superuser",)
    search_fields = ("username", "email", "first_name", "last_name", "phone_number")
    readonly_fields = ("id",)
    fieldsets = (
        ("User Information", {
            "fields": ("id", "username", "email", "first_name", "last_name", "phone_number")
        }),
        ("Permissions", {
            "fields": ("is_superuser",)
        }),
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "product_count")
    search_fields = ("name",)
    
    def product_count(self, obj):
        count = obj.products.count()
        return count
    product_count.short_description = "Number of Products"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "image_thumbnail", "title", "brand", "price", "stock", "stock_status")
    list_filter = ("brand", "stock")
    search_fields = ("title", "description", "brand__name")
    readonly_fields = ("id", "image_preview")
    fieldsets = (
        ("Basic Information", {
            "fields": ("id", "title", "brand", "description")
        }),
        ("Pricing & Inventory", {
            "fields": ("price", "stock")
        }),
        ("Image", {
            "fields": ("image", "image_preview")
        }),
    )
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "No Image"
    image_thumbnail.short_description = "Image"
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; object-fit: contain;" />',
                obj.image.url
            )
        return "No image uploaded"
    image_preview.short_description = "Preview"
    
    def stock_status(self, obj):
        stock = obj.stock or 0
        if stock == 0:
            return format_html('<span style="color: red; font-weight: bold;">Out of Stock</span>')
        elif stock < 10:
            return format_html('<span style="color: orange; font-weight: bold;">Low Stock ({})</span>', stock)
        else:
            return format_html('<span style="color: green;">In Stock ({})</span>', stock)
    stock_status.short_description = "Stock Status"


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity", "is_ordered", "subtotal", "created_at", "updated_at")
    list_filter = ("is_ordered", "created_at", "updated_at")
    search_fields = ("user__username", "user__email", "product__title")
    readonly_fields = ("id", "created_at", "updated_at", "subtotal_display")
    date_hierarchy = "created_at"
    
    def subtotal(self, obj):
        price = float(obj.product.price) if obj.product else 0
        return f"₹{price * obj.quantity:.2f}"
    subtotal.short_description = "Subtotal"
    
    def subtotal_display(self, obj):
        price = float(obj.product.price) if obj.product else 0
        return f"₹{price * obj.quantity:.2f}"
    subtotal_display.short_description = "Subtotal"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "item_total")
    
    def item_total(self, obj):
        if obj.product:
            price = float(obj.product.price) if obj.product.price else 0
            return f"₹{price * obj.quantity:.2f}"
        return "₹0.00"
    item_total.short_description = "Total"


@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "order_number", "user", "contact_number", "payment_method", "is_paid", "total_amount", "item_count", "created_at")
    list_filter = ("is_paid", "payment_method", "created_at")
    search_fields = ("id", "user__username", "user__email", "contact_number", "shipping_address")
    readonly_fields = ("id", "created_at", "total_display", "items_display")
    date_hierarchy = "created_at"
    inlines = [OrderItemInline]
    
    fieldsets = (
        ("Order Information", {
            "fields": ("id", "user", "created_at")
        }),
        ("Shipping Details", {
            "fields": ("shipping_address", "contact_number")
        }),
        ("Payment Information", {
            "fields": ("payment_method", "payment_reference", "is_paid")
        }),
        ("Order Summary", {
            "fields": ("total_display", "items_display"),
            "classes": ("collapse",)
        }),
    )
    
    def order_number(self, obj):
        return f"#{obj.id}"
    order_number.short_description = "Order #"
    
    def total_amount(self, obj):
        total = 0
        for item in obj.items.all():
            if item.product:
                price = float(item.product.price) if item.product.price else 0
                total += price * item.quantity
        return f"₹{total:.2f}"
    total_amount.short_description = "Total"
    
    def total_display(self, obj):
        total = 0
        for item in obj.items.all():
            if item.product:
                price = float(item.product.price) if item.product.price else 0
                total += price * item.quantity
        return f"₹{total:.2f}"
    total_display.short_description = "Total Amount"
    
    def items_display(self, obj):
        items_list = []
        for item in obj.items.all():
            if item.product:
                price = float(item.product.price) if item.product.price else 0
                items_list.append(f"{item.product.title} x {item.quantity} = ₹{price * item.quantity:.2f}")
        return format_html("<br/>".join(items_list)) if items_list else "No items"
    items_display.short_description = "Items"
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = "Items"


# Customize admin site headers
admin.site.site_header = "Watch Store Administration"
admin.site.site_title = "Watch Store Admin"
admin.site.index_title = "Welcome to Watch Store Administration"
