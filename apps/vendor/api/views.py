from rest_framework.views import APIView 
from rest_framework.response import Response
from vendor.models import Vendor
from .serializers import VendorSerializer
from scripts.api_utils import FormattedResponseData

class SearchVendor(APIView):
    
    def get(self, request):
        try:
            searched_name = request.query_params['vendor-name']
            vendors = Vendor.objects.filter(name__icontains = searched_name)
            ser = VendorSerializer(vendors, many=True)
            return Response(data=FormattedResponseData(data=ser.data, msg="Working"))
        except Vendor.DoesNotExist:
            return Response(data={'msg':'No Vendor', 'data':None})


class VendorDetail(APIView):
    def get(self, request):
        try:
            vendor = Vendor.objects.get(name = request.query_params['vendor-name'])
            ser = VendorSerializer(vendor)
            return Response(data={'err''msg':'good', 'data':ser.data})
        except Vendor.DoesNotExist:
            return Response(data={'msg':'No Vendor', 'data':None})

        except Exception as e:
            return Response(data={'msg':'No Vendor', 'data':None})


