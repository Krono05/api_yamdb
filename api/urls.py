from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet


router = DefaultRouter(trailing_slash=False)

API_V = 'v1'

router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)

urlpatterns = [
    path(f'{API_V}/', include(router.urls)),
]
