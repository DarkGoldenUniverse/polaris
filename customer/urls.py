from django.urls import include, path

urlpatterns = [
    path("v2/", include(("customer.v2.urls", "customer"), namespace="v2")),
]
