from django.db.models import Q
from rest_framework import generics

from inventory.models import Category, Inventory
from inventory.v2.serializers import CategorySerializer, InventorySerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        path = self.request.query_params.get("path")
        if path is not None:
            queryset = queryset.filter(path__startswith=path)
        else:
            queryset = queryset.all()

        return queryset


class InventoryListAPIView(generics.ListAPIView):
    queryset = Inventory.objects.filter(visible=True).order_by("code")
    serializer_class = InventorySerializer
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.query_params.get("category")
        if category is not None:
            queryset = queryset.filter(category__path__startswith=category)

        name = self.request.query_params.get("name")
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        code = self.request.query_params.get("code")
        if code is not None:
            queryset = queryset.filter(code__icontains=code)

        search = self.request.query_params.get("search")
        if search is not None:
            queryset = queryset.filter(
                Q(category__path__startswith=search) | Q(code__icontains=search) | Q(name__icontains=search)
            )

        return queryset
