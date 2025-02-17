from django.urls import path
from notifications.views import SubscribeForNewsLetter


app_name = "notification"
urlpatterns = [
    path('subscribe_newsletter/',SubscribeForNewsLetter.as_view(), name='subscribe_newsletter'),
]

