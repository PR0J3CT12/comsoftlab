from comsoftlab.apps.front.consumers import MailConsumer
from django.urls import re_path


websocket_urlpatterns = [
    re_path(r'ws/progress/(?P<uid>\w+)/$', MailConsumer.as_asgi()),
]