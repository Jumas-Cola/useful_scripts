from django.shortcuts import render
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item
from .serializers import ItemSerializer


class ItemView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response({'items': serializer.data})

    def post(self, request):
        item = request.data.get('item')
        serializer = ItemSerializer(data=item)
        if serializer.is_valid(raise_exception=True):
            item_saved = serializer.save()
        return Response({"success": "Item '{}' created successfully".format(item_saved.field)})

    def put(self, request, pk):
        saved_item = get_object_or_404(Item.objects.all(), pk=pk)
        data = request.data.get('item')
        serializer = ItemSerializer(instance=saved_item, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            item_saved = serializer.save()

        return Response({"success": "Item '{}' updated successfully".format(item_saved.field)})

    def delete(self, request, pk):
        item = get_object_or_404(Item.objects.all(), pk=pk)
        item.delete()
        return Response({
            "message": "Item with id `{}` has been deleted.".format(pk)
        }, status=204)
