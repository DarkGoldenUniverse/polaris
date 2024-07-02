from django.urls import path, include

urlpatterns = [
    path("accounts/", include(("account.v2.identity.urls", "account"), namespace="identity")),
]
