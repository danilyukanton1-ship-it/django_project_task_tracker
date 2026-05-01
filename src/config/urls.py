from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# JWT urls
jwt_urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# API urls
api_urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/users/", include("account.v1.urls")),
    path("api/tasks/", include("task_manager.v1.urls")),
]


# DRF SPECTACULAR SWAGGER urls
drf_spectacular_urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path(
            "",
            include("task_manager.urls"),
        ),
        path("", include("django.contrib.auth.urls")),
    ]
    + jwt_urlpatterns
    + api_urlpatterns
    + drf_spectacular_urlpatterns
)

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls() + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
