# store/serializers.py
from rest_framework import serializers
from .models import (
    UserAccount, Brand, Product,
    ShoppingCart, CustomerOrder, OrderItem
)

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = "__all__"
        read_only_fields = ("id",)

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "name")

class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Brand.objects.all(), source="brand")
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ("id", "brand", "brand_id", "title", "description", "price", "image", "stock")

class ShoppingCartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Product.objects.all(), source="product")

    class Meta:
        model = ShoppingCart
        fields = ("id", "user", "product", "product_id", "quantity", "is_ordered", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Product.objects.all(), source="product")

    class Meta:
        model = OrderItem
        fields = ("id", "product", "product_id", "quantity")

class CustomerOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = CustomerOrder
        fields = ("id", "user", "shipping_address", "contact_number", "payment_method", "payment_reference", "is_paid", "created_at", "items")
        read_only_fields = ("id", "created_at", "items")

class CustomerOrderCreateSerializer(serializers.ModelSerializer):
    # Accept nested items for order creation
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = CustomerOrder
        fields = ("id", "user", "shipping_address", "contact_number", "payment_method", "payment_reference", "is_paid", "items")
        read_only_fields = ("id",)

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        order = CustomerOrder.objects.create(**validated_data)
        for item in items_data:
            product = item.get("product")
            quantity = item.get("quantity", 1)
            
            # Check and reduce stock
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for {product.title}. Available: {product.stock}, Requested: {quantity}"
                )
            
            # Reduce stock
            product.stock -= quantity
            product.save()
            
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
        return order
