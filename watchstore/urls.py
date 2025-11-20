"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# store/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import (
    UserAccountViewSet, BrandViewSet, ProductViewSet,
    ShoppingCartViewSet, CustomerOrderViewSet
)

router = routers.DefaultRouter()
router.register(r"users", UserAccountViewSet)
router.register(r"brands", BrandViewSet)
router.register(r"products", ProductViewSet)
router.register(r"cart", ShoppingCartViewSet, basename="cart")
router.register(r"orders", CustomerOrderViewSet, basename="orders")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
