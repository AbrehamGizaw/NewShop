from rest_framework import serializers
from rest_framework.serializers import ModelSerializer 
from core.models import SocialMedia

class SerializedPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """ A custom PrimaryKeyRelatedField that uses 'id' field on CREATE method and serializes the data on READ. """

    def __init__(self, model_serializer, **kwargs):
        self.model_serializer = model_serializer
        super().__init__(**kwargs)

    def to_representation(self, value):
        """
        Serialize the related object using the specified serializer class.
        """
        if isinstance(value, self.get_queryset().model):
            instance = value
        else:
            instance = self.get_queryset().get(pk=value.pk)

        serializer = self.model_serializer(instance, context=self.context)
        return serializer.data


class SocialMediaSerializer(ModelSerializer):
    class Meta:
        model = SocialMedia 
        fields = ['id','name', 'icon', 'link']
        read_only_fields = ['id']
        
        