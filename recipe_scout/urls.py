from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("recipe.api.urls")),
    path("account/", include("account.api.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
