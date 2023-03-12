from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Admin of genres."""
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    empty_value_display = 'None value'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin of categories."""

    list_display = ('name', 'slug',)
    list_display_links = ('name',)
    search_fields = ('name', 'slug',)
    empty_value_display = 'None value'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Admin of titles."""
    list_display = ("name", "year", "category",)
    list_filter = ("year", "genre", "category")
    search_fields = ("name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'score', 'pub_date')
    list_filter = ('title', 'author', 'pub_date')
    search_fields = (
        'title__name',
        'author__username',
    )
    list_editable = ('score',)


@admin.register(Comment)
class CommentClass(admin.ModelAdmin):
    """Admin of comments."""

    list_display = ('text', 'review', 'author', 'pub_date',)
    list_filter = ('review', 'author', 'pub_date',)
    list_editable = ('text',)
    search_fields = ('review', 'author', 'pub_date',)
    empty_value_display = 'None value'
