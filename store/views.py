from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem_set.count() > 0:
            return Response({'error': 'Product cannot be deleted as its associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        product_count=Count('product')).all()
    serializer_class = CollectionSerializer


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(
        product_count=Count('product')).all()
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.product_set.count() > 0:
            return Response({'error': 'The Collection cannot be deleted as it is associated with one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

\
