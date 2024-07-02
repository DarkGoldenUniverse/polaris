from django.urls import path

from order.v2.admin.views import AdminOrderListAPIView

urlpatterns = [
    path("orders", AdminOrderListAPIView.as_view(), name="orders"),
]
