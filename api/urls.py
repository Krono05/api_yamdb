from rest_framework.routers import DefaultRouter
from django.urls import path, include
from api.views import (CategoryViewSet, GenreViewSet, TitleViewSet, ReviewsViewSet, CommentsViewSet, 
                        UserViewSet, send_code, send_token)



router = DefaultRouter()
API_V = 'v1'

router.register(r'users', UserViewSet)
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
    path(f'{API_V}/auth/token/', send_token),
    path(f'{API_V}/auth/email/',
         send_code),
    path(f'{API_V}/', include(router.urls)),

]
