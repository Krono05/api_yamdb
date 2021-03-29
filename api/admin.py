from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Genre, Title, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'bio', 'confirmation_code', 'role')


admin.site.register(User, UserAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category')
    search_fields = ('name', 'year')
    list_filter = ('genre', 'category')
    empty_value_display = '-пусто-'
