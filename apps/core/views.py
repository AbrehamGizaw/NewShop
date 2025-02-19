from django.shortcuts import render
from django.views.generic import View
from vendor.models import Vendor, VendorCategory
from core.models import WhyUsItem
from core.serialize import *
from notifications.models import Newsletter
from django.db.models import Q

class Index(View):
    def get(self, *args, **kwargs):
        vendors = Vendor.objects.filter(is_live = True)
        vendor_cats = VendorCategory.objects.all()
        whyus = WhyUsItem.objects.filter(is_published = True)
        news = Newsletter.objects.all()[:5] #Fetch top 5 only

        return render(self.request, "index.html", {"vendor_cats":vendor_cats,
                                                   "vendors":vendors, 
                                                   "whyus":whyus,
                                                   "news":news
                                                    }
                                                )

def SearchItem(request):
    queryString = request.GET.get('query',);
    categories = VendorCategory.objects.all();
    vendors = Vendor.objects.filter(Q(name__icontains = queryString) | Q(category__name__icontains = queryString))
    return render(request, "core/search.html",{'searchquery':queryString, 
                                               'vendors':vendors,
                                               'categories':categories})    


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class WhyUsItemList(APIView):
     def get(self, request):
          whyusitem = WhyUsItem.objects.all()
          serializer = WhyUsItemSerializer(whyusitem, many = True)
          return Response(serializer.data)

class WhyUsItemCreate(APIView):
     def post(self, request):
          serializer = WhyUsItemSerializer(data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WhyUsItemDetail(APIView):
     def get_by_pk(self, pk):
          try:
               return WhyUsItem.objects.get(pk=pk)
          except:
               return Response({
                    'error':'There is no such whyusitem'
               }, status=status.HTTP_404_NOT_FOUND )
    
     def get(self, request, pk):
          whyusitem = self.get_by_pk(pk)
          serializer = WhyUsItemSerializer(whyusitem)
          return Response(serializer.data)
     
     def put(self, request, pk):
          whyusitem = self.get_by_pk(pk)
          serializer = WhyUsItemSerializer(whyusitem, data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
     
     def delete(self, request, pk):
          whyusitem = self.get_by_pk(pk)
          whyusitem.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)
     


class TermsAndConditionsList(APIView):
     def get(self, request):
          termsandconditions = TermsAndConditions.objects.all()
          serializer = TermsAndConditionsSerializer(termsandconditions, many = True)
          return Response(serializer.data)

class TermsAndConditionsCreate(APIView):
     def post(self, request):
          serializer = TermsAndConditionsSerializer(data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TermsAndConditionsDetail(APIView):
     def get_by_pk(self, pk):
          try:
               return TermsAndConditions.objects.get(pk=pk)
          except:
               return Response({
                    'error':'There is no such termsandconditions'
               }, status=status.HTTP_404_NOT_FOUND )
    
     def get(self, request, pk):
          termsandconditions = self.get_by_pk(pk)
          serializer = TermsAndConditionsSerializer(termsandconditions)
          return Response(serializer.data)
     
     def put(self, request, pk):
          termsandconditions = self.get_by_pk(pk)
          serializer = TermsAndConditionsSerializer(termsandconditions, data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
     
     def delete(self, request, pk):
          termsandconditions = self.get_by_pk(pk)
          termsandconditions.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)



class SocialMediaList(APIView):
     def get(self, request):
          socialmedia = SocialMedia.objects.all()
          serializer = SocialMediaSerializer(socialmedia, many = True)
          return Response(serializer.data)

class SocialMediaCreate(APIView):
     def post(self, request):
          serializer = SocialMediaSerializer(data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SocialMediaDetail(APIView):
     def get_by_pk(self, pk):
          try:
               return SocialMedia.objects.get(pk=pk)
          except:
               return Response({
                    'error':'There is no such socialmedia'
               }, status=status.HTTP_404_NOT_FOUND )
    
     def get(self, request, pk):
          socialmedia = self.get_by_pk(pk)
          serializer = SocialMediaSerializer(socialmedia)
          return Response(serializer.data)
     
     def put(self, request, pk):
          socialmedia = self.get_by_pk(pk)
          serializer = SocialMediaSerializer(socialmedia, data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
     
     def delete(self, request, pk):
          socialmedia = self.get_by_pk(pk)
          socialmedia.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)
