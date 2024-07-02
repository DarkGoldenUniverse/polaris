from django.urls import path

from account.v2.resource.views import UserDetailApiView

urlpatterns = [
    path("users/me", UserDetailApiView.as_view(), name="users-me"),
]
