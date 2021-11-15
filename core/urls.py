from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Jungle Devs Challenge",
        default_version="v1",
        description="Simplified version of a news provider API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api/", include("news.urls")),
    path("api/", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns += [path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0)),]
