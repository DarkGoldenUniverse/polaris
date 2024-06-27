from django.urls import path

from account.views import UserDetailApiView, UserLoginAPIView, UserLogoutAPIView

urlpatterns = []

api = [
    path("api/accounts/me", UserDetailApiView.as_view(), name="me"),
    path("api/accounts/login", UserLoginAPIView.as_view(), name="login"),
    path("api/accounts/logout", UserLogoutAPIView.as_view(), name="logout"),
]

urlpatterns += api
