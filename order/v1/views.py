from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics

from inventory.models import Category, Inventory
from inventory.v1.serializers import CategorySerializer, InventorySerializer
from order.models import Order


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        path = self.request.query_params.get("path")
        if path is not None:
            queryset = queryset.filter(path__startswith=path)
        else:
            queryset = queryset.all()

        return queryset
