from django.urls import path

from customer.v2.admin.views import AdminCustomerListCreateAPIView, AdminCustomerDetailAPIView

urlpatterns = [
    path("customers", AdminCustomerListCreateAPIView.as_view(), name="customer_list_create"),
    path("customers/<int:pk>", AdminCustomerDetailAPIView.as_view(), name="customer_detail"),
]
