from django.db import models


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
