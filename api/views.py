from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, permissions, filters

from .models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .filters import TitleFilterSet


class CategoryViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GenreViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilterSet
