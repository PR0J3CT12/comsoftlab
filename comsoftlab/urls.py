from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from comsoftlab.apps.front.consumers import MailConsumer

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="comsoftlab API",
        default_version='1.0.0',
        description="API documentation of comsoftlab",
    ),
    public=True,
    url=''
)

urlpatterns = [
    path('app/', include('front.urls')),
    path('api/user/', include('users.urls')),
    path('api/docs', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
]

websocket_urlpatterns = [
    path('ws/progress/', MailConsumer.as_asgi()),
]
