from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilterSet
from .mixins import (BaseCreateListDestroyMixin,
                     BaseCreateListRetrieveUpdateDestroyMixin)
from .models import Category, Genre, Review, Title, User
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrModOrAdmin
from .serializers import (CategorySerializer, CommentSerializer,
                          EmailConfirmCodeSerializer, EmailSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleInputSerializer, TitleResultSerializer,
                          UserSerializer)


class CategoryViewSet(BaseCreateListDestroyMixin, viewsets.GenericViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GenreViewSet(BaseCreateListDestroyMixin, viewsets.GenericViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class TitleViewSet(BaseCreateListRetrieveUpdateDestroyMixin,
                   viewsets.GenericViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('id')
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleResultSerializer
        return TitleInputSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthorOrModOrAdmin, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthorOrModOrAdmin, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, pk=review_id, title__id=title_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()


@api_view(['POST'])
def send_code(request):
    """Регистрация пользователя по email и генерация кода."""
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    username = serializer.data.get('username')
    user = User.objects.get_or_create(email=email, username=username)[0]
    confirm_code = PasswordResetTokenGenerator().make_token(user)
    serializer = UserSerializer(
        user, data={'confirmation_code': confirm_code}, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    send_mail('Регистрация на YaMDB', f'Ваш код: {confirm_code}',
              settings.FROM_EMAIL, [email], fail_silently=False)
    return Response({'email': email})


@api_view(['POST'])
def send_token(request):
    """Получения токена по email и коду доступа."""
    def get_token(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    serializer = EmailConfirmCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    confirm_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    if user.confirmation_code == confirm_code:
        response = {'token': get_token(user)}
        return Response(response, status=status.HTTP_200_OK)
    response = {'confirmation_code': 'Неверный код для данного email'}
    return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    pagination_class = PageNumberPagination

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,),
            methods=['get', 'patch'], url_path='me')
    def get_or_update_self(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                instance=request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data)
