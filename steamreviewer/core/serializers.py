from rest_framework import serializers
from .models import (
    Games, Reviews, Genres, Developers, GameSystemRequirements,
    Users, UserSpecs, UserWishList, UserFavoritedGenres, UserLibrary
)


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'


class DevelopersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developers
        fields = '__all__'


class GameSystemRequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSystemRequirements
        fields = ['cpu_requirements', 'gpu_requirements', 'ram_requirements']


class GamesListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for game lists"""
    genre_name = serializers.CharField(source='genre.genre_name', read_only=True)
    price = serializers.DecimalField(source='game_price', max_digits=10, decimal_places=2, read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    total_reviews = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Games
        fields = ['game_id', 'game_name', 'genre_name', 'price', 'discount_percentage', 
                  'rating', 'total_reviews', 'release_year', 'storage_gb']
    
    def get_discount_percentage(self, obj):
        # TODO: Add discount logic when discount data is available
        return 0
    
    def get_rating(self, obj):
        # Calculate rating from positive review ratio if available
        if hasattr(obj, 'positive_review_ratio') and obj.positive_review_ratio is not None:
            return round(obj.positive_review_ratio * 10, 1)
        return 7.5  # Default rating


class GamesDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with relationships"""
    genre_name = serializers.CharField(source='genre.genre_name', read_only=True)
    price = serializers.DecimalField(source='game_price', max_digits=10, decimal_places=2, read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    total_reviews = serializers.IntegerField(read_only=True)
    positive_reviews = serializers.IntegerField(read_only=True)
    system_requirements = serializers.SerializerMethodField()
    
    class Meta:
        model = Games
        fields = ['game_id', 'game_name', 'genre_name', 'price', 'discount_percentage',
                  'rating', 'total_reviews', 'positive_reviews', 'release_year', 
                  'storage_gb', 'system_requirements']
    
    def get_discount_percentage(self, obj):
        return 0
    
    def get_rating(self, obj):
        if hasattr(obj, 'positive_review_ratio') and obj.positive_review_ratio is not None:
            return round(obj.positive_review_ratio * 10, 1)
        return 7.5
    
    def get_system_requirements(self, obj):
        try:
            req = obj.gamesystemrequirements
            return {
                'cpu': req.cpu_requirements,
                'gpu': req.gpu_requirements,
                'ram': req.ram_requirements,
                'storage': f"{obj.storage_gb} GB" if obj.storage_gb else None,
                'os': 'Windows',  # Default for Steam games
                'directx': None  # Not in current schema
            }
        except GameSystemRequirements.DoesNotExist:
            return None


class ReviewsSerializer(serializers.ModelSerializer):
    game_id = serializers.IntegerField(source='game.game_id', read_only=True)
    user_id = serializers.SerializerMethodField()
    hours_played = serializers.FloatField(source='author_playtime_forever', read_only=True)
    date_posted = serializers.DateTimeField(source='created_at', read_only=True)
    sentiment = serializers.SerializerMethodField()
    
    class Meta:
        model = Reviews
        fields = ['review_id', 'game_id', 'user_id', 'review_text', 'sentiment', 
                  'hours_played', 'date_posted']
    
    def get_user_id(self, obj):
        # Return a placeholder user ID since Reviews don't have user FK
        return 1
    
    def get_sentiment(self, obj):
        if obj.voted_up is True:
            return 'Positive'
        elif obj.voted_up is False:
            return 'Negative'
        return 'Neutral'



class ReviewsListSerializer(serializers.ModelSerializer):
    """Lighter serializer for review lists (truncated text)"""
    game_name = serializers.CharField(source='game.game_name', read_only=True)
    review_preview = serializers.SerializerMethodField()
    
    class Meta:
        model = Reviews
        fields = ['review_id', 'game_name', 'review_preview', 'voted_up', 'votes_up', 'votes_funny', 'word_count', 'author_playtime_forever', 'created_at']
    
    def get_review_preview(self, obj):
        return obj.review_text[:150] + '...' if len(obj.review_text) > 150 else obj.review_text


class UserSpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSpecs
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    specs = UserSpecsSerializer(source='userspecs', read_only=True)
    
    class Meta:
        model = Users
        fields = '__all__'


class UserWishListSerializer(serializers.ModelSerializer):
    game = GamesListSerializer(read_only=True)
    game_id = serializers.IntegerField(write_only=True, required=False)
    user_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = UserWishList
        fields = ['user', 'game', 'user_id', 'game_id']
    
    def create(self, validated_data):
        # Handle both 'game' and 'game_id' fields
        game_id = validated_data.pop('game_id', None)
        user_id = validated_data.pop('user_id', None)
        
        if game_id:
            validated_data['game_id'] = game_id
        if user_id:
            validated_data['user_id'] = user_id
            
        return super().create(validated_data)


class UserLibrarySerializer(serializers.ModelSerializer):
    game = GamesListSerializer(read_only=True)
    
    class Meta:
        model = UserLibrary
        fields = '__all__'
