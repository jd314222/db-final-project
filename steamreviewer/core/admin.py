from django.contrib import admin
from .models import (
    Genres, Developers, Games, GameSystemRequirements, Users,
    UserSpecs, UserWishList, UserFavoritedGenres, CreatedGames, Reviews
)


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ['genre_id', 'genre_name']
    search_fields = ['genre_name']


@admin.register(Developers)
class DevelopersAdmin(admin.ModelAdmin):
    list_display = ['developer_id', 'developer_name']
    search_fields = ['developer_name']


@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    list_display = ['game_id', 'game_name', 'genre', 'game_price', 'release_year', 'storage_gb']
    list_filter = ['genre', 'release_year']
    search_fields = ['game_name']


@admin.register(GameSystemRequirements)
class GameSystemRequirementsAdmin(admin.ModelAdmin):
    list_display = ['game', 'cpu_requirements', 'gpu_requirements', 'ram_requirements']
    search_fields = ['game__game_name']


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'budget']


@admin.register(UserSpecs)
class UserSpecsAdmin(admin.ModelAdmin):
    list_display = ['user', 'cpu', 'gpu', 'ram']


@admin.register(UserWishList)
class UserWishListAdmin(admin.ModelAdmin):
    list_display = ['user', 'game']
    list_filter = ['user']


@admin.register(UserFavoritedGenres)
class UserFavoritedGenresAdmin(admin.ModelAdmin):
    list_display = ['user', 'genre']
    list_filter = ['genre']


@admin.register(CreatedGames)
class CreatedGamesAdmin(admin.ModelAdmin):
    list_display = ['developer', 'game', 'date_created']
    list_filter = ['developer', 'date_created']


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['review_id', 'game', 'voted_up', 'votes_up', 'created_at']
    list_filter = ['voted_up', 'created_at']
    search_fields = ['review_text', 'game__game_name']
