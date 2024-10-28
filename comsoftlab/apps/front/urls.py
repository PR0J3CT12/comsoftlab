from django.urls import path
from . import views

urlpatterns = [
    path('emails/<int:uid>', views.emails_view, name='emails page'),
]
