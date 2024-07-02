from django.urls import include, path

urlpatterns = [
    path("v2/", include(("account.v2.urls", "account"), namespace="v2")),
]
