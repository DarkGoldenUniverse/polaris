from rest_framework import generics

from order.models import Order
from order.v2.serializers import OrderSerializer


class AdminOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.query_params.get("status")
        if status is not None:
            queryset = queryset.filter(status__in=status)
        else:
            queryset = queryset.all()

        return queryset
