from rest_framework import serializers

from django.db.models import Avg

from .models import Category, Genre, Title, Comment, Review, User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'slug']
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'slug']
        model = Genre


class TitleResultSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'name', 'year', 'rating', 'description', 'genre',
                  'category']
        model = Title

    def get_rating(self, obj):
        return obj.reviews.aggregate(rating=Avg('score')).get('rating')


class TitleInputSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        exclude = ['title']
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        exclude = ['review']
        model = Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'bio',)
        model = User
