from django.urls import path

from order.v2.admin.views import AdminOrderListCreateAPIView

urlpatterns = [
    path("orders", AdminOrderListCreateAPIView.as_view(), name="order_list_create"),
]
