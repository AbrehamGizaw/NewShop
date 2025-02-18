from rest_framework import serializers
from .models import *
from django.forms import ValidationError

class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = ['created_at', 'updated_at', 'removed_at']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:  
        model = Image
        fields = ['id', 'file', 'name', 'checksum']

class TagCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TagCategory
        fields = ['id', 'name']
 
class NewsTagSerializer(serializers.ModelSerializer):
    category = TagCategorySerializer(read_only=True)
    class Meta:
        model = NewsTag
        fields = ['id', 'name', 'slug', 'description', 'category', 'is_active' ]

class NewsletterSerializer(serializers.ModelSerializer):
    images = serializers.SlugRelatedField(slug_field='name', queryset=Image.objects.all(), many=True)
    tags = serializers.SlugRelatedField(slug_field='name', queryset=NewsTag.objects.all(), many=True)
    
    is_published = serializers.BooleanField(default=False)

    class Meta:
        model = Newsletter
        fields = ['id', 'title', 'slug', 'content', 'images', 'tags', 'is_published', 'publication_date', 'created_at', 'updated_at', 'removed_at']

    def validate_publication_date(self, value):
        # Ensure that if the newsletter is not published, no publication date is set
        is_published = self.initial_data.get('is_published', None)
        if is_published is not None and not is_published and value is not None:
            raise serializers.ValidationError("Unpublished newsletters should not have a publication date.")
        return value
    

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['id', 'email', 'last_news_sent_date', 'subscription_date', 'email_verified_at', 'is_active', 'created_at', 'updated_at', 'removed_at']

    def validate_email(self, value):
        # Explicitly validate the email format using the model's method
        instance = self.instance or Subscriber(email=value)  # Create an instance to call the method
        instance.email = value
        instance.validate_email_format()  # Call the custom validation method
        return value
    

class NewsletterSentSerializer(serializers.ModelSerializer):
    subscriber = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all())
    newsletter = serializers.PrimaryKeyRelatedField(queryset=Newsletter.objects.all())
    status = serializers.ChoiceField(choices=Status.get_status_choices(), default=Status.SENT.value)

    class Meta:
        model = NewsletterSent
        fields = ['subscriber', 'newsletter', 'sent_date', 'status']
        read_only_fields = ['sent_date']