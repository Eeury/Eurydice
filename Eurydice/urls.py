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

# Serve media files locally when not using Cloudinary (shared hosting, development)
# In production with shared hosting, configure your web server (Apache/Nginx) to serve /media/
# For development or when not using Cloudinary, Django will serve media files
USE_CLOUDINARY = bool(getattr(settings, 'USE_CLOUDINARY', False))
if settings.DEBUG or not USE_CLOUDINARY:
    if hasattr(settings, 'MEDIA_ROOT') and settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


