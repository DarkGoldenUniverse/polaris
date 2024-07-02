from django.urls import path

from account.v2.identity.views import UserLoginAPIView, UserLogoutAPIView

urlpatterns = [
    path("login", UserLoginAPIView.as_view(), name="login"),
    path("logout", UserLogoutAPIView.as_view(), name="logout"),
]
