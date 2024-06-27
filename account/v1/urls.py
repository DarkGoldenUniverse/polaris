from django.urls import path

from account.v1.views import UserDetailApiView, UserLoginAPIView, UserLogoutAPIView

urlpatterns = [
    path("accounts/me", UserDetailApiView.as_view(), name="me"),
    path("accounts/login", UserLoginAPIView.as_view(), name="login"),
    path("accounts/logout", UserLogoutAPIView.as_view(), name="logout"),
]
