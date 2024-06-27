"""
URL configuration for polaris project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# API
urlpatterns = [
    path("api/v1/", include(("account.v1.urls", "account"), namespace="accounts.v1")),
    path("api/v1/", include(("inventory.v1.urls", "inventory"), namespace="inventories.v1")),
]

# Page
urlpatterns += [
    path("admin/", admin.site.urls),
]

# Swagger
urlpatterns += [
    path("", SpectacularSwaggerView.as_view(), name="swagger"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("redoc/", SpectacularRedocView.as_view(), name="redoc"),
]

# File
urlpatterns += [
    path("favicon.ico", RedirectView.as_view(url="static/favicon/favicon-32x32.png", permanent=True)),
    path("apple-touch-icon.png", RedirectView.as_view(url="static/favicon/apple-touch-icon.png", permanent=True)),
]
