from django.urls import path

from account.v2.identity.views import UserDetailApiView, UserLoginAPIView, UserLogoutAPIView

urlpatterns = [
    path("me", UserDetailApiView.as_view(), name="me"),
    path("login", UserLoginAPIView.as_view(), name="login"),
    path("logout", UserLogoutAPIView.as_view(), name="logout"),
]
