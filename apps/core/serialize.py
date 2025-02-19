from rest_framework import serializers
from .models import WhyUsItem, TermsAndConditions, SocialMedia

class WhyUsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyUsItem
        fields = ['id', 'title', 'content', 'icon', 'is_published', 'created_at', 'updated_at', 'removed_at']
        read_only_fields = ['created_at', 'updated_at', 'removed_at']  

class TermsAndConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndConditions
        fields = ['id', 'content', 'created_at', 'updated_at', 'removed_at']
        read_only_fields = ['created_at', 'updated_at', 'removed_at']  

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['id', 'name', 'icon', 'link', 'created_at', 'updated_at', 'removed_at']
        read_only_fields = ['created_at', 'updated_at', 'removed_at']  
