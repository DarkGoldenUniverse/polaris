from django.urls import path, include

urlpatterns = [
    path("resource/", include(("inventory.v2.resource.urls", "inventory"), namespace="resource")),
]
