from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class UserRole(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER
    )
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField('E-mail', unique=True)
    confirmation_code = models.CharField(max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    class Meta:
        ordering = ('username',)

class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=100
    )
    slug = models.SlugField(
        verbose_name='Slug категории',
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=100
    )
    slug = models.SlugField(
        verbose_name='Slug жанра',
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Title(models.Model):
    name = models.CharField(
        verbose_name='Произведение',
        max_length=200
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        blank=True,
        null=True
    )

    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        blank=True,
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(blank=True, null=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.SmallIntegerField(blank=False, null=False)
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE
    )
    text = models.TextField(blank=False, null=False),
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
