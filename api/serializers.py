from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Genre


class TitleResultSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.FloatField()

    class Meta:
        fields = '__all__'
        model = Title


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

    def validate(self, attrs):
        request = self.context['request']
        if request.data == {}:
            raise serializers.ValidationError('Нет данных')
        view = self.context['view']
        title_id = view.kwargs.get('title_id')
        user = request.user
        review = Review.objects.filter(
            author=user,
            title_id=title_id
        ).exists()
        if review and request.method == 'POST':
            raise serializers.ValidationError('Отзыв уже есть')
        return attrs

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
        fields = ('username', 'first_name', 'last_name',
                  'email', 'role', 'bio',)
        model = User

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()

class EmailConfirmCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=100)