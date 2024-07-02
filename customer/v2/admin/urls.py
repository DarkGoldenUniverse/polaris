from django.urls import path

from account.v2.resource.views import UserDetailApiView

urlpatterns = [
    path("customers", UserDetailApiView.as_view(), name="customers"),
]
