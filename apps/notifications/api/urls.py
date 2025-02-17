from django.urls import path
from rest_framework import routers 

from notifications.api.views import NewsLetterApi, SubscribeApi

router = routers.DefaultRouter()
router.register(r'news', NewsLetterApi)

urlpatterns = [
    path("subscribe/", SubscribeApi.as_view(), name="subscribe_newsletter"),
]
urlpatterns += router.urls

