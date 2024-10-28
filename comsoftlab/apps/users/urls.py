from django.urls import path
from . import views

urlpatterns = [
    path('get-messages/<int:uid>', views.get_messages, name='get user messages'),
]
