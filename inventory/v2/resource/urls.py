from django.urls import path

from inventory.v2.resource.views import CategoryListAPIView, InventoryListAPIView

urlpatterns = [
    path("inventories", InventoryListAPIView.as_view(), name="inventory-list"),
    path("categories", CategoryListAPIView.as_view(), name="category-list"),
]
