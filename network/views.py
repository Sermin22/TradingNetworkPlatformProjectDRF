from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import NetworkLink, Product
from .serializers import NetworkLinkSerializer, ProductSerializer
from .permissions import IsActiveEmployee


class NetworkLinkViewSet(viewsets.ModelViewSet):
    queryset = NetworkLink.objects.all()
    serializer_class = NetworkLinkSerializer
    permission_classes = [IsActiveEmployee,]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country']
    search_fields = ['name', 'email', 'city', 'country']
    ordering_fields = ['created_at', 'debt_to_supplier']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployee,]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['model']
    search_fields = ['name', 'model']
    ordering_fields = ['release_date']
