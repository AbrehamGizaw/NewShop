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






# 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Subscriber, Newsletter, NewsletterSent, NewsTag, BaseModel, TagCategory, Image
from .serializer import SubscriberSerializer, NewsletterSerializer, NewsletterSentSerializer, NewsTagSerializer, BaseModelSerializer, TagCategorySerializer, ImageSerializer

class SubscriberList(APIView):
     def get(self, request):
          subscriber = Subscriber.objects.all()
          serializer = SubscriberSerializer(subscriber, many = True)
          return Response(serializer.data)

class SubscriberCreate(APIView):
     def post(self, request):
          serializer = SubscriberSerializer(data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubscriberDetail(APIView):
     def get_by_pk(self, request, pk):
          try:
               return Subscriber.objects.get(pk=pk)
          except:
               return Response({
                    'error':'There is no such subscriber'
               }, status=status.HTTP_404_NOT_FOUND )
    
     def get(self, request, pk):
          subscriber = self.get_by_pk(pk)
          serializer = SubscriberSerializer(subscriber)
          return Response(serializer.data)
     
     def put(self, request, pk):
          subscriber = self.get_by_pk(pk)
          serializer = SubscriberSerializer(subscriber, data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
     
     def delete(self, request, pk):
          subscriber = self.get_by_pk(pk)
          subscriber.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)



class ImageList(APIView):
    def get(self, request):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

class ImageCreate(APIView):
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageDetail(APIView):
    def get_by_id(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return None

    def get(self, request, pk):
        image = self.get_by_id(pk)
        if image:
            serializer = ImageSerializer(image)
            return Response(serializer.data)
        return Response({
            'error': "Image not found"
        }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        image = self.get_by_id(pk)
        if image:
            serializer = ImageSerializer(image, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'error': "Image not found"
        }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        image = self.get_by_id(pk)
        if image:
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'error': "Image not found"
        }, status=status.HTTP_404_NOT_FOUND)




class NewsletterList(APIView):
     def get(self, request):
          newsletter = Newsletter.objects.all()
          serializer = NewsletterSerializer(newsletter, many = True)
          return Response(serializer.data)
    
class NewsletterCreate(APIView):
     def post(self, request):
          serializer = NewsletterSerializer(data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
class NewsletterDetail(APIView):
     def get_by_id(self, pk):
          try:
               return Newsletter.objects.get(pk=pk)
          except:
               return Response({
                    'error':"There is no such data"
               }, status=status.HTTP_404_NOT_FOUND)
     def get(self, request, pk):
          newsletter = self.get_by_id(pk)
          serializer = NewsletterSerializer(newsletter)
          return Response(serializer.data)
     def put(self, request, pk):
          newsletter = self.get_by_id(pk)
          serializer = NewsletterSerializer(newsletter, data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     def delete(self, request, pk):
          newsletter = self.get_by_id(pk)
          newsletter.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)

class NewsletterSentList(APIView):
     def get(self, request):
          newslettersent = NewsletterSent.objects.all()
          serilizer = NewsletterSentSerializer(newslettersent, many=True)
          return Response(newslettersent.data)

class NewsletterSentCreate(APIView):
     def post(self, request):
          serializer = NewsletterSentSerializer(data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsletterSentDetail(APIView):
     def get_by_id(self, request, pk):
          try:
               return NewsletterSent.objects.get(pk=pk)
          except:
               return Response({
                    'error':'There is no such file'
               }, status=status.HTTP_404_NOT_FOUND)
     def get(self, request, pk):
          newslettersent = self.get_by_id(pk)
          serializer = NewsletterSentSerializer(newslettersent)
          return Response(serializer.data)
     def put(self, request, pk):
          newsletter = self.get_by_id(pk)
          serializer = NewsletterSentSerializer(newsletter, data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     def delete(self, request, pk):
          newslettersent = self.get_by_id(pk)
          newslettersent.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)
     



class NewsTagList(APIView):
     def get(self, request):
          newstag = NewsTag.objects.all()
          serializer = NewsTagSerializer(newstag, many = True)
          return Response(serializer.data)

class NewsTagCreate(APIView):
     def post(self, request):
          serializer = NewsTagSerializer(data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsTagDetail(APIView):
     def get_by_pk(self, request, pk):
          try:
               return NewsTag.objects.get(pk=pk)
          except:
               return Response({
                    'error':'There is no such file of newstag'
               }, status=status.HTTP_404_NOT_FOUND )
    
     def get(self, request, pk):
          newstag = self.get_by_pk(pk)
          serializer = NewsTagSerializer(newstag)
          return Response(serializer.data)
     
     def put(self, request, pk):
          newstag = self.get_by_pk(pk)
          serializer = NewsTagSerializer(newstag, data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
     
     def delete(self, request, pk):
          newstag = self.get_by_pk(pk)
          newstag.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)



class TagCategoryList(APIView):
     def get(self, request):
          tagcategory = TagCategory.objects.all()
          serializer = TagCategorySerializer(tagcategory, many = True)
          return Response(serializer.data)

class TagCategoryCreate(APIView):
     def post(self, request):
          serializer = TagCategorySerializer(data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagCategoryDetail(APIView):
     def get_by_pk(self, request, pk):
          try:
               return TagCategory.objects.get(pk=pk)
          except:
               return Response({
                    'error':'There is no such file'
               }, status=status.HTTP_404_NOT_FOUND )
    
     def get(self, request, pk):
          tagcategory = self.get_by_pk(pk)
          serializer = TagCategorySerializer(tagcategory)
          return Response(serializer.data)
     
     def put(self, request, pk):
          tagcategory = self.get_by_pk(pk)
          serializer = TagCategorySerializer(tagcategory, data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
     
     def delete(self, request, pk):
          tagcategory = self.get_by_pk(pk)
          tagcategory.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)



