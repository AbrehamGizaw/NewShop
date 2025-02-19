from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError
from django.utils import timezone
class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = ['created_at', 'updated_at', 'removed_at']
        read_only_fields = ['created_at', 'updated_at', 'removed_at']
    
class VendorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorCategory
        fields = ['id', 'name', 'created_at', 'updated_at', 'removed_at']
        read_only_fields = ['created_at', 'updated_at', 'removed_at']


class VendorSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=VendorCategory.objects.all(), many=True)
    
    logo = serializers.ImageField()

    class Meta:
        model = Vendor
        fields = [
            'id', 'name', 'content', 'logo', 'categories', 'is_live', 'is_top', 
            'publication_date', 'created_at', 'updated_at', 'removed_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'removed_at']


class VendorAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorAddress
        fields = [
            'id', 'name', 'country', 'state', 'city', 'location', 'is_hq',
            'created_at', 'updated_at', 'removed_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'removed_at']



class VendorSocialMediaSerializer(serializers.ModelSerializer):
    vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())
    social_media = serializers.PrimaryKeyRelatedField(queryset=SocialMedia.objects.all())

    class Meta:
        model = VendorSocialMedia
        fields = ['id', 'vendor', 'social_media', 'address', 'created_at', 'updated_at', 'removed_at']
        read_only_fields = ['created_at', 'updated_at', 'removed_at']


class VendorContentSerializer(serializers.ModelSerializer):
    vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all(), many = False)

    class Meta:
        model = VendorContent
        fields = ['id', 'vendor', 'header', 'content', 'icon', 'created_at', 'updated_at', 'removed_at']
        read_only_fields = ['created_at', 'updated_at', 'removed_at']


class VendorWhySerializer(serializers.ModelSerializer):
    vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())
    class Meta:
        model = VendorWhy
        fields = ['id', 'vendor', 'header', 'content', 'icon', 'created_at', 'updated_at', 'removed_at']
        read_only_fields = ['created_at', 'updated_at', 'removed_at']


class VendorLookingSerializer(serializers.ModelSerializer):
    vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())
    icon = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())

    class Meta:
        model = VendorLooking
        fields = ['id', 'vendor', 'header', 'content', 'icon', 'created_at', 'updated_at', 'removed_at']
        read_only_fields = ['created_at', 'updated_at', 'removed_at']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'file', 'name', 'checksum', 'created_at', 'updated_at', 'removed_at']
        read_only_fields = ['created_at', 'updated_at', 'removed_at', 'checksum']


