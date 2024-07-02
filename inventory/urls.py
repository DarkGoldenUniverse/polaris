from django.urls import include, path

urlpatterns = [
    path("v2/", include(("inventory.v2.urls", "inventory"), namespace="v2")),
]
