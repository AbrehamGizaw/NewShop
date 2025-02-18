from django.shortcuts import render


# 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import VendorCategory, Vendor, VendorAddress, VendorSocialMedia, VendorContent, VendorWhy, VendorLooking, Image
from .serializer import *

class VendorList(APIView):
     def get(self, request):
          vendor = Vendor.objects.all()
          serializer = VendorSerializer(vendor, many = True)
          return Response(serializer.data)

class VendorCreate(APIView):
     def post(self, request):
          serializer = VendorSerializer(data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorDetail(APIView):
     def get_by_pk(self, pk):
          try:
               return Vendor.objects.get(pk=pk)
          except:
               return Response({
                    'error':'There is no such vendor'
               }, status=status.HTTP_404_NOT_FOUND )
    
     def get(self, request, pk):
          vendor = self.get_by_pk(pk)
          serializer = VendorSerializer(vendor)
          return Response(serializer.data)
     
     def put(self, request, pk):
          vendor = self.get_by_pk(pk)
          serializer = VendorSerializer(vendor, data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
     
     def delete(self, request, pk):
          vendor = self.get_by_pk(pk)
          vendor.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)




class VendorCategoryList(APIView):
     def get(self, request):
          vendorcategory = VendorCategory.objects.all()
          serializer = VendorCategorySerializer(vendorcategory, many = True)
          return Response(serializer.data)

class VendorCategoryCreate(APIView):
     def post(self, request):
          serializer = VendorCategorySerializer(data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorCategoryDetail(APIView):
     def get_by_pk(self, pk):
          try:
               return VendorCategory.objects.get(pk=pk)
          except:
               return Response({
                    'error':'There is no such vendorcategory'
               }, status=status.HTTP_404_NOT_FOUND )
    
     def get(self, request, pk):
          vendorcategory = self.get_by_pk(pk)
          serializer = VendorCategorySerializer(vendorcategory)
          return Response(serializer.data)
     
     def put(self, request, pk):
          vendorcategory = self.get_by_pk(pk)
          serializer = VendorCategorySerializer(vendorcategory, data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
     
     def delete(self, request, pk):
          vendorcategory = self.get_by_pk(pk)
          vendorcategory.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)




class VendorAddressList(APIView):
     def get(self, request):
          vendoraddress = VendorAddress.objects.all()
          serializer = VendorAddressSerializer(vendoraddress, many = True)
          return Response(serializer.data)

class VendorAddressCreate(APIView):
     def post(self, request):
          serializer = VendorAddressSerializer(data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorAddressDetail(APIView):
     def get_by_pk(self, pk):
          try:
               return VendorAddress.objects.get(pk=pk)
          except:
               return Response({
                    'error':'There is no such vendoradress'
               }, status=status.HTTP_404_NOT_FOUND )
    
     def get(self, request, pk):
          vendoraddress = self.get_by_pk(pk)
          serializer = VendorAddressSerializer(vendoraddress)
          return Response(serializer.data)
     
     def put(self, request, pk):
          vendoraddress = self.get_by_pk(pk)
          serializer = VendorAddressSerializer(vendoraddress, data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
     
     def delete(self, request, pk):
          vendoraddress = self.get_by_pk(pk)
          vendoraddress.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)




class VendorSocialMediaList(APIView):
     def get(self, request):
          vendorsocialmedia = VendorSocialMedia.objects.all()
          serializer = VendorSocialMediaSerializer(vendorsocialmedia, many = True)
          return Response(serializer.data)

class VendorSocialMediaCreate(APIView):
     def post(self, request):
          serializer = VendorSocialMediaSerializer(data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorSocialMediaDetail(APIView):
     def get_by_pk(self, pk):
          try:
               return VendorSocialMedia.objects.get(pk=pk)
          except:
               return Response({
                    'error':'There is no such vendorsocialmedia'
               }, status=status.HTTP_404_NOT_FOUND )
    
     def get(self, request, pk):
          vendorsocialmedia = self.get_by_pk(pk)
          serializer = VendorSocialMediaSerializer(vendorsocialmedia)
          return Response(serializer.data)
     
     def put(self, request, pk):
          vendorsocialmedia = self.get_by_pk(pk)
          serializer = VendorSocialMediaSerializer(vendorsocialmedia, data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
     
     def delete(self, request, pk):
          vendorsocialmedia = self.get_by_pk(pk)
          vendorsocialmedia.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)




class VendorContentList(APIView):
     def get(self, request):
          vendorcontent = VendorContent.objects.all()
          serializer = VendorContentSerializer(vendorcontent, many = True)
          return Response(serializer.data)

class VendorContentCreate(APIView):
     def post(self, request):
          serializer = VendorContentSerializer(data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorContentDetail(APIView):
     def get_by_pk(self, pk):
          try:
               return VendorContent.objects.get(pk=pk)
          except:
               return Response({
                    'error':'There is no such vendorcontent'
               }, status=status.HTTP_404_NOT_FOUND )
    
     def get(self, request, pk):
          vendorcontent = self.get_by_pk(pk)
          serializer = VendorContentSerializer(vendorcontent)
          return Response(serializer.data)
     
     def put(self, request, pk):
          vendorcontent = self.get_by_pk(pk)
          serializer = VendorContentSerializer(vendorcontent, data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
     
     def delete(self, request, pk):
          vendorcontent = self.get_by_pk(pk)
          vendorcontent.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)





class VendorWhyList(APIView):
     def get(self, request):
          vendorwhy = VendorWhy.objects.all()
          serializer = VendorWhySerializer(vendorwhy, many = True)
          return Response(serializer.data)

class VendorWhyCreate(APIView):
     def post(self, request):
          serializer = VendorWhySerializer(data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorWhyDetail(APIView):
     def get_by_pk(self, pk):
          try:
               return VendorWhy.objects.get(pk=pk)
          except:
               return Response({
                    'error':'There is no such vendorwhy'
               }, status=status.HTTP_404_NOT_FOUND )
    
     def get(self, request, pk):
          vendorwhy = self.get_by_pk(pk)
          serializer = VendorWhySerializer(vendorwhy)
          return Response(serializer.data)
     
     def put(self, request, pk):
          vendorwhy = self.get_by_pk(pk)
          serializer = VendorWhySerializer(vendorwhy, data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
     
     def delete(self, request, pk):
          vendorwhy = self.get_by_pk(pk)
          vendorwhy.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)




class ImageList(APIView):
     def get(self, request):
          image = Image.objects.all()
          serializer = ImageSerializer(image, many = True)
          return Response(serializer.data)

class ImageCreate(APIView):
     def post(self, request):
          serializer = ImageSerializer(data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageDetail(APIView):
     def get_by_pk(self, pk):
          try:
               return Image.objects.get(pk=pk)
          except:
               return Response({
                    'error':'There is no such image'
               }, status=status.HTTP_404_NOT_FOUND )
    
     def get(self, request, pk):
          image = self.get_by_pk(pk)
          serializer = ImageSerializer(image)
          return Response(serializer.data)
     
     def put(self, request, pk):
          image = self.get_by_pk(pk)
          serializer = ImageSerializer(image, data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
     
     def delete(self, request, pk):
          image = self.get_by_pk(pk)
          image.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)



class ImageList(APIView):
     def get(self, request):
          vendorlooking = Image.objects.all()
          serializer = ImageSerializer(vendorlooking, many = True)
          return Response(serializer.data)

class ImageCreate(APIView):
     def post(self, request):
          serializer = ImageSerializer(data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageDetail(APIView):
     def get_by_pk(self, pk):
          try:
               return Image.objects.get(pk=pk)
          except:
               return Response({
                    'error':'There is no such vendorlooking'
               }, status=status.HTTP_404_NOT_FOUND )
    
     def get(self, request, pk):
          vendorlooking = self.get_by_pk(pk)
          serializer = ImageSerializer(vendorlooking)
          return Response(serializer.data)
     
     def put(self, request, pk):
          vendorlooking = self.get_by_pk(pk)
          serializer = ImageSerializer(vendorlooking, data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
     
     def delete(self, request, pk):
          vendorlooking = self.get_by_pk(pk)
          vendorlooking.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)

