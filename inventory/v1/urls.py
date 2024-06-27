from django.urls import path

from inventory.v1.views import CategoryListAPIView, InventoryListAPIView

urlpatterns = [
    path("categories", CategoryListAPIView.as_view(), name="category"),
    path("inventories", InventoryListAPIView.as_view(), name="inventory"),
]
