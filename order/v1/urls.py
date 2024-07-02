from django.urls import path

from inventory.v1.views import CategoryListAPIView, InventoryListAPIView

urlpatterns = [
    path("orders", CategoryListAPIView.as_view(), name="category"),
]
