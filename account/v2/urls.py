from django.urls import path, include

urlpatterns = [
    path("identity/", include(("account.v2.identity.urls", "account"), namespace="identity")),
    path("resource/", include(("account.v2.resource.urls", "account"), namespace="resource")),
]
