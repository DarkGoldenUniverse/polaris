from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from order.models import Order, ORDER_STATUS_MAPPING
from order.v2.admin.serializers import AdminOrderSerializer, AdminOrderItemSerializer

# Create an inverted mapping dictionary
INVERTED_ORDER_STATUS_MAPPING = {code: status for status, code in ORDER_STATUS_MAPPING}


class AdminOrderListAPIView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = AdminOrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        status_params = self.request.query_params.getlist("status")
        if status_params is not None and len(status_params) > 0:
            # Map the status strings to their corresponding codes
            status_codes = [INVERTED_ORDER_STATUS_MAPPING[status] for status in status_params]
            # Filter the queryset by the mapped status codes
            queryset = queryset.filter(status__in=status_codes)
        else:
            queryset = queryset.all()

        return queryset

    def post(self, request, *args, **kwargs):
        items_data = request.data.pop("items")
        order_serializer = self.get_serializer(data=request.data)

        if order_serializer.is_valid():
            order = order_serializer.save(created_by=request.user)
            for item_data in items_data:
                item_data["order"] = order.id

                item_serializer = AdminOrderItemSerializer(data=item_data)
                if item_serializer.is_valid():
                    item_serializer.save(created_by=request.user)
                else:
                    order.delete()

                    return Response(item_serializer.errors, status=HTTP_400_BAD_REQUEST)
            return Response(order_serializer.data, status=HTTP_201_CREATED)
        return Response(order_serializer.errors, status=HTTP_400_BAD_REQUEST)
