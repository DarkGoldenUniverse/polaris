from django.urls import path, include

urlpatterns = [
    path("admin/", include(("customer.v2.admin.urls", "customer"), namespace="admin")),
]
