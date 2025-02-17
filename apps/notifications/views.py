from django.views import View
from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import redirect
from rest_framework import viewsets
from .models import Subscriber, Newsletter 
from .api.serializers import NewsLetterSerializer

class SubscribeForNewsLetter(View):
    def get(self, *args, **kwargs):
        return redirect('/')
    
    def post(self, *args, **kwargs):
        email = self.request.POST.get('email')
        success, msg = Subscriber.toggle_or_create_subscription(email, True)
        
        print(msg)
        # If sent from footer section or somewhere else using ajax request
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse(data={'error': False, 'message': msg, })
        
        # Requests initiated from pages
        x = messages.success(self.request, msg)
        return redirect("/")
    

class NewsLetterApi(viewsets.ModelViewSet):
     queryset = Newsletter.objects.all()
     serializer_class = NewsLetterSerializer

