from rest_framework import serializers 
from ..models import Newsletter, NewsTag, Image
from core.api.serializers import SerializedPrimaryKeyRelatedField

class NewsTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsTag
        fields = ['id', 'name', 'slug', 'description', 'category']
        read_only_fields = ['id']
        exclude_fields = ['removed_at']


class NotificationImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'name', 'file']
        read_only_fields = ['id']
        exclude_fields = ['removed_at']


class NewsLetterSerializer(serializers.ModelSerializer):
    images = SerializedPrimaryKeyRelatedField(queryset=Image.objects.all(),  many=True, model_serializer = NotificationImageSerializer  )
    tags = SerializedPrimaryKeyRelatedField(queryset=NewsTag.objects.filter(is_active=True), many=True, model_serializer = NewsTagSerializer)

    class Meta:
        model = Newsletter
        fields = ['id','title','slug','content','images','tags','is_published','publication_date', 'created_at']
        read_only_fields = ['id']
        