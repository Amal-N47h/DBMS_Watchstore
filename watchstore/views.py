# store/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserAccount, Brand, Product, ShoppingCart, CustomerOrder, OrderItem
from .serializers import (
    UserAccountSerializer, BrandSerializer, ProductSerializer,
    ShoppingCartSerializer, CustomerOrderSerializer, CustomerOrderCreateSerializer, OrderItemSerializer
)
from django.db.models import F

class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all().order_by("id")
    serializer_class = UserAccountSerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all().order_by("name")
    serializer_class = BrandSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("brand").all().order_by("id")
    serializer_class = ProductSerializer

class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.select_related("product", "user").all().order_by("-updated_at")
    serializer_class = ShoppingCartSerializer

    def create(self, request, *args, **kwargs):
        # Create or increment cart item for same user & product if user given
        user = request.data.get("user", None)
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if product_id is None:
            return Response({"detail": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        filters = {"product_id": product_id, "is_ordered": False}
        if user:
            filters["user_id"] = user
        else:
            # leave user null for guest
            filters["user__isnull"] = True

        existing = ShoppingCart.objects.filter(**filters).first()
        if existing:
            existing.quantity = F("quantity") + quantity
            existing.save()
            existing.refresh_from_db()
            serializer = self.get_serializer(existing)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def clear_ordered(self, request):
        # optionally mark cart items for a user as ordered (or delete)
        user = request.data.get("user", None)
        qs = ShoppingCart.objects.filter(is_ordered=True)
        if user:
            qs = ShoppingCart.objects.filter(user_id=user, is_ordered=True)
        deleted, _ = qs.delete()
        return Response({"deleted": deleted})

class CustomerOrderViewSet(viewsets.ModelViewSet):
    queryset = CustomerOrder.objects.prefetch_related("items__product").all().order_by("-created_at")

    def get_serializer_class(self):
        if self.action in ("create",):
            return CustomerOrderCreateSerializer
        return CustomerOrderSerializer
