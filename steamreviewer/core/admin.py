from django.contrib import admin
from .models import (
    Genres, Developers, Games, GameSystemRequirements, Users,
    UserSpecs, UserWishList, UserFavoritedGenres, CreatedGames, Reviews,
    UserLibrary, Tags, GameTags, GameUrls, Languages, GameImages,
    Platform, GamePlatform, Publishers, GamePublishers
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


@admin.register(UserLibrary)
class UserLibraryAdmin(admin.ModelAdmin):
    list_display = ['user', 'game', 'purchase_date', 'price_paid']
    list_filter = ['purchase_date']
    search_fields = ['user__user_id', 'game__game_name']


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['tag_id', 'tag_string']
    search_fields = ['tag_string']


@admin.register(GameTags)
class GameTagsAdmin(admin.ModelAdmin):
    list_display = ['game', 'tag']
    list_filter = ['tag']
    search_fields = ['game__game_name', 'tag__tag_string']


@admin.register(GameUrls)
class GameUrlsAdmin(admin.ModelAdmin):
    list_display = ['game', 'url']
    search_fields = ['game__game_name']


@admin.register(Languages)
class LanguagesAdmin(admin.ModelAdmin):
    list_display = ['game', 'language_supported']
    list_filter = ['language_supported']
    search_fields = ['game__game_name']


@admin.register(GameImages)
class GameImagesAdmin(admin.ModelAdmin):
    list_display = ['game', 'image_url']
    search_fields = ['game__game_name']


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['plat_id', 'platform_name']
    search_fields = ['platform_name']


@admin.register(GamePlatform)
class GamePlatformAdmin(admin.ModelAdmin):
    list_display = ['game', 'platform']
    list_filter = ['platform']
    search_fields = ['game__game_name']


@admin.register(Publishers)
class PublishersAdmin(admin.ModelAdmin):
    list_display = ['pub_id', 'publisher']
    search_fields = ['publisher']


@admin.register(GamePublishers)
class GamePublishersAdmin(admin.ModelAdmin):
    list_display = ['game', 'publisher', 'publish_date']
    list_filter = ['publisher', 'publish_date']
    search_fields = ['game__game_name', 'publisher__publisher']
    search_fields = ['review_text', 'game__game_name']
