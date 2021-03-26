from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet, ReviewsViewSet, CommentsViewSet


router = DefaultRouter(trailing_slash=False)

API_V = 'v1'

router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
urlpatterns = [
    path(f'{API_V}/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        f'{API_V}/token/refresh/',
        TokenRefreshView.as_view(), name='token_refresh'
    ),
    path(f'{API_V}', include(router.urls)),
]
