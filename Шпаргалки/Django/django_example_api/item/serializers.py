from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.Serializer):
    field = serializers.CharField(max_length=255)
    author_id = serializers.IntegerField()

    def create(self, validated_data):
        return Item.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.field = validated_data.get('field', instance.field)
        instance.author_id = validated_data.get('author_id', instance.author_id)

        instance.save()
        return instance
