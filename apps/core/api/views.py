from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from rest_framework.request import Request
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from core.models import SocialMedia
from scripts.api_utils import FormattedResponseData
from core.api.serializers import SocialMediaSerializer
from vendor.models import (
    Vendor,
    VendorCategory,
    VendorContent,
    VendorLooking,
    VendorSocialMedia,
    VendorWhy,
)
from vendor.api.serializers import (
    VendorSerializer,
    VendorCategorySerializer,
    VendorContentSerializer,
    VendorWhySerializer,
    VendorLookingSerializer,
)


class Index(APIView):
    def get(self, request):
        serialized = VendorSerializer(Vendor.objects.all(), many=True)
        return Response(data={"msg": "This is the message", "data": serialized.data})


class SocialMedias(viewsets.ModelViewSet):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer

class JoinForm(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        social_medias = SocialMedia.objects.all()
        social_ser = SocialMediaSerializer(social_medias, many=True)

        categories = VendorCategory.objects.all()
        category_ser = VendorCategorySerializer(categories, many=True)

        return Response(
            data=FormattedResponseData(
                data={
                    "social_medias": social_ser.data,
                    "vendor_categories": category_ser.data,
                }
            )
        )

    def post(self, request:Request):
        vendor_ser = VendorSerializer(data=request.data)
        if vendor_ser.is_valid():
            
            obj = vendor_ser.create(validated_data=vendor_ser.validated_data, request=request)
            return Response(
                data=FormattedResponseData(msg = "Successfully registered vendor! ", 
                                           data = VendorSerializer(obj).data, ),
                status=status.HTTP_200_OK,
            )

        print("errors : ", vendor_ser.errors)
        return Response(
            data=FormattedResponseData(
                err=True,
                msg="Form validation Error!",
                data=vendor_ser.errors,
            ),
            
        )


class VendorView(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

