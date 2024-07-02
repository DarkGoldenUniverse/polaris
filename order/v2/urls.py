from django.urls import include, path

urlpatterns = [
    path("admin/", include(("order.v2.admin.urls", "order"), namespace="admin")),
]
