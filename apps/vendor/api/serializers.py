import json
from rest_framework import serializers
from rest_framework.request import Request
from vendor.models import (
    VendorCategory,
    Vendor,
    Image,
    VendorContent,
    VendorLooking,
    VendorSocialMedia,
    VendorWhy,
)
from core.models import SocialMedia
from core.api.serializers import SocialMediaSerializer, SerializedPrimaryKeyRelatedField

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["name", "file"]


class VendorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorCategory
        fields = ["id", "name"]
        read_only_fields = ["id"]


class VendorContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorContent
        fields = "__all__"
        read_only_fields = ["id"]


class VendorWhySerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorWhy
        fields = ["id", "header", "content", "icon"]
        read_only_fields = ["id"]


class VendorLookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorLooking
        fields = "__all__"
        read_only_fields = ["id"]


class VendorSocialMediaSerializer(serializers.ModelSerializer):
    social_media = SerializedPrimaryKeyRelatedField(queryset=SocialMedia.objects.all(), model_serializer = SocialMediaSerializer)
    class Meta:
        model = VendorSocialMedia
        fields = "__all__"
        read_only_fields = ["id"]


class VendorSerializer(serializers.ModelSerializer):
    category = SerializedPrimaryKeyRelatedField(
        queryset=VendorCategory.objects.all(), model_serializer=VendorCategorySerializer
    )

    contents = VendorContentSerializer(
        source="vendorcontent_set", many=True, read_only=True
    )
    social_medias = VendorSocialMediaSerializer(
        source="vendorsocialmedia_set", many=True, read_only=True
    )
    whys = VendorWhySerializer(source="vendorwhy_set", many=True, read_only=True)
    looking = VendorLookingSerializer(
        source="vendorlooking_set", many=True, read_only=True
    )

    class Meta:
        model = Vendor
        fields = [
            "id",
            "name",
            "content",
            "logo",
            "category",
            "social_medias",
            "whys",
            "looking",
            "contents",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data, request: Request):
        # Create the main Vendor instance
        vendor = Vendor.objects.create(**validated_data)

        # Fetch every data 
        contentImages = request.FILES.getlist("contentImages")
        contents = json.loads(request.data.get("contents", []))
        social_medias_data = json.loads(request.data.get("social_medias", []))
        whys_data = json.loads(request.data.get("whys", []))
        looking_data = json.loads(request.data.get("lookings", []))

        for content in contents:
            iconFile = contentImages [ int(content.get("icon")) ]
            content['icon'] = iconFile
            VendorContent.objects.create(vendor=vendor, **content)

        
        for social_media_data in social_medias_data:
            social_media_obj = SocialMedia.objects.get(id=social_media_data['social_media'])
            VendorSocialMedia.objects.create(vendor=vendor, social_media= social_media_obj, address=social_media_data['address'])

        # Create VendorWhy instances
        for why_data in whys_data:
            VendorWhy.objects.create(vendor=vendor, **why_data)

        for looking in looking_data:
            VendorLooking.objects.create(vendor=vendor, **looking)

        return vendor

    def update(self, instance, validated_data):
        return instance


class VendorContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorContent
        fields = "__all__"
        read_only_fields = ["id"]
