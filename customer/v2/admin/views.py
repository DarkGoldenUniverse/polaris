from rest_framework.generics import ListCreateAPIView, RetrieveAPIView

from customer.models import Customer
from customer.v2.admin.serializers import AdminCustomerSerializer


class AdminCustomerListCreateAPIView(ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = AdminCustomerSerializer


class AdminCustomerDetailAPIView(RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = AdminCustomerSerializer
