from django.urls import path
from account.v1.views import UserAPIView, UserDetailAPIView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("", UserAPIView.as_view()),
    path("<int:pk>/", UserDetailAPIView.as_view()),
]
