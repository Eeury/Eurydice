from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from shop import views as shop_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", shop_views.login_modal, name="login"),
    path("", include("shop.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    # JWT Auth endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


