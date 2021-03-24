from .models import Title, Review
from .serializers import ReviewSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets


class ReviewsViewSet(viewsets.GenericViewSet):
    serializer_class = ReviewSerializer
    lookup_field = 'id'

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()


class CommentsViewSet(viewsets.GenericViewSet):
    serializer_class = CommentSerializer
    lookup_field = 'id'

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()
