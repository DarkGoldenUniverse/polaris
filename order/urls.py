from django.urls import include, path

urlpatterns = [
    path("v2/", include(("order.v2.urls", "order"), namespace="v2")),
]
