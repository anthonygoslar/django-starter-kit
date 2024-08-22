from django.contrib import admin
from django.urls import path

from drf_yasg import openapi #new foe swagger
from drf_yasg.views import get_schema_view as swagger_get_schema_view #new foe swagger


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Your Project APIs",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
]
