from rest_framework import viewsets 
from rest_framework.views import APIView
from rest_framework.response import Response
from notifications.models import Newsletter, Subscriber
from notifications.api.serializers import NewsLetterSerializer 
from scripts.api_utils import FormattedResponseData

class NewsLetterApi(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsLetterSerializer


class SubscribeApi(APIView):
    
    def post(self, *args, **kwargs):
        print(self.request.POST)
        email = self.request.POST.get('email')
        subscriber, created = Subscriber.objects.get_or_create(email = email)
        msg = "Successfully Subscribed!" if created else "Already Subscribed"
        return  Response(data=FormattedResponseData(msg = msg))
