from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Q, F, Case, When, FloatField
from django_filters.rest_framework import DjangoFilterBackend

from .models import Games, Reviews, Genres, Developers, Users, UserWishList, UserSpecs
from .serializers import (
    GamesListSerializer, GamesDetailSerializer, ReviewsSerializer,
    GenresSerializer, DevelopersSerializer, UsersSerializer, UserWishListSerializer, UserSpecsSerializer
)


class GamesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for browsing and filtering games
    
    Filters: price, genre, release_year, search by name
    """
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genre', 'release_year']
    search_fields = ['game_name']
    ordering_fields = ['game_price', 'release_year']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GamesDetailSerializer
        return GamesListSerializer
    
    def get_queryset(self):
        # Annotate with review stats
        queryset = Games.objects.select_related('genre').annotate(
            total_reviews=Count('reviews'),
            positive_reviews=Count('reviews', filter=Q(reviews__voted_up=True)),
            positive_review_ratio=Case(
                When(total_reviews__gt=0, 
                     then=F('positive_reviews') * 1.0 / F('total_reviews')),
                default=0.75,
                output_field=FloatField()
            )
        ).order_by('-total_reviews')
        
        # Filter by price range
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        
        if price_min:
            queryset = queryset.filter(game_price__gte=price_min)
        if price_max:
            queryset = queryset.filter(game_price__lte=price_max)
        
        # Filter by budget categories
        budget = self.request.query_params.get('budget')
        if budget == 'free':
            queryset = queryset.filter(game_price=0)
        elif budget == 'under_10':
            queryset = queryset.filter(game_price__lte=10)
        elif budget == 'under_20':
            queryset = queryset.filter(game_price__lte=20)
        elif budget == 'under_30':
            queryset = queryset.filter(game_price__lte=30)
        
        # Filter by genre name
        genre_name = self.request.query_params.get('genre')
        if genre_name:
            queryset = queryset.filter(genre__genre_name__iexact=genre_name)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get overall game statistics"""
        stats = Games.objects.aggregate(
            total_games=Count('game_id'),
            avg_price=Avg('game_price'),
            games_with_price=Count('game_id', filter=Q(game_price__isnull=False))
        )
        return Response(stats)


class ReviewsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for browsing reviews
    
    Filters: game_id, game name search, voted_up (sentiment), ordering by helpfulness
    """
    queryset = Reviews.objects.select_related('game').order_by('-created_at')
    serializer_class = ReviewsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['game']
    search_fields = ['game__game_name']
    ordering_fields = ['votes_up', 'votes_funny', 'created_at', 'author_playtime_forever']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by game_id
        game_id = self.request.query_params.get('game_id')
        if game_id:
            queryset = queryset.filter(game_id=game_id)
        
        # Filter by sentiment
        sentiment = self.request.query_params.get('sentiment')
        if sentiment:
            if sentiment.lower() == 'positive':
                queryset = queryset.filter(voted_up=True)
            elif sentiment.lower() == 'negative':
                queryset = queryset.filter(voted_up=False)
        
        return queryset


class GenresViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for game genres"""
    queryset = Genres.objects.annotate(
        game_count=Count('games')
    ).order_by('-game_count')
    serializer_class = GenresSerializer


class DevelopersViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for game developers"""
    queryset = Developers.objects.all()
    serializer_class = DevelopersSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['developer_name']


class UsersViewSet(viewsets.ModelViewSet):
    """API endpoint for user profiles - allows creating new users"""
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']


class UserSpecsViewSet(viewsets.ModelViewSet):
    """API endpoint for user system specs"""
    queryset = UserSpecs.objects.all()
    serializer_class = UserSpecsSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']


class UserWishListViewSet(viewsets.ModelViewSet):
    """API endpoint for user wishlists - add/remove games from wishlist"""
    queryset = UserWishList.objects.select_related('user', 'game')
    serializer_class = UserWishListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']
    
    def create(self, request, *args, **kwargs):
        """Add a game to user's wishlist"""
        user_id = request.data.get('user') or request.data.get('user_id')
        game_id = request.data.get('game') or request.data.get('game_id')
        
        if not user_id or not game_id:
            return Response(
                {'detail': 'Both user and game are required'},
                status=400
            )
        
        # Check if already in wishlist
        if UserWishList.objects.filter(user_id=user_id, game_id=game_id).exists():
            return Response(
                {'detail': 'Game already in wishlist'},
                status=400
            )
        
        # Create the wishlist entry
        wishlist_item = UserWishList.objects.create(
            user_id=user_id,
            game_id=game_id
        )
        
        serializer = self.get_serializer(wishlist_item)
        return Response(serializer.data, status=201)
    
    def destroy(self, request, *args, **kwargs):
        """Remove a game from user's wishlist"""
        # Support lookup by user_game combination
        user_id = self.kwargs.get('pk', '').split('_')[0] if '_' in self.kwargs.get('pk', '') else None
        game_id = self.kwargs.get('pk', '').split('_')[1] if '_' in self.kwargs.get('pk', '') else None
        
        if user_id and game_id:
            try:
                wishlist_item = UserWishList.objects.get(user_id=user_id, game_id=game_id)
                wishlist_item.delete()
                return Response(status=204)
            except UserWishList.DoesNotExist:
                return Response({'detail': 'Not found'}, status=404)
        
        return super().destroy(request, *args, **kwargs)


class ReviewAnalyticsViewSet(viewsets.ViewSet):
    """
    API endpoint for review analytics and insights
    Provides statistical analysis of reviews and games
    """
    
    @action(detail=False, methods=['get'])
    def top_reviewed(self, request):
        """Games with the most reviews"""
        games = Games.objects.annotate(
            total_reviews=Count('reviews'),
            positive_reviews=Count('reviews', filter=Q(reviews__voted_up=True)),
            positive_review_ratio=Case(
                When(total_reviews__gt=0, 
                     then=F('positive_reviews') * 1.0 / F('total_reviews')),
                default=0.0,
                output_field=FloatField()
            )
        ).filter(
            total_reviews__gt=0
        ).order_by('-total_reviews')[:10]
        
        data = [{
            'game_id': game.game_id,
            'game_name': game.game_name,
            'total_reviews': game.total_reviews,
            'positive_reviews': game.positive_reviews,
            'rating': round(game.positive_review_ratio * 10, 1),
            'image_url': game.gameimages_set.first().image_url if game.gameimages_set.exists() else None
        } for game in games]
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def best_value(self, request):
        """Games with best rating per dollar (value score)"""
        from django.db.models.functions import Ln
        
        games = Games.objects.annotate(
            total_reviews=Count('reviews'),
            positive_reviews=Count('reviews', filter=Q(reviews__voted_up=True)),
            positive_review_ratio=Case(
                When(total_reviews__gt=0, 
                     then=F('positive_reviews') * 1.0 / F('total_reviews')),
                default=0.0,
                output_field=FloatField()
            )
        ).filter(
            total_reviews__gte=10,  # Must have at least 10 reviews
            game_price__gt=0,  # Exclude free games
            game_price__lte=100  # Reasonable price cap
        ).order_by('-positive_review_ratio', '-total_reviews')[:10]
        
        data = [{
            'game_id': game.game_id,
            'game_name': game.game_name,
            'price': float(game.game_price),
            'rating': round(game.positive_review_ratio * 10, 1),
            'total_reviews': game.total_reviews,
            'value_score': round((game.positive_review_ratio * 10) / float(game.game_price), 2),
            'image_url': game.gameimages_set.first().image_url if game.gameimages_set.exists() else None
        } for game in games]
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def most_wishlisted(self, request):
        """Games most frequently added to wishlists"""
        from .models import UserWishList
        
        games = Games.objects.annotate(
            wishlist_count=Count('userwishlist'),
            total_reviews=Count('reviews'),
            positive_reviews=Count('reviews', filter=Q(reviews__voted_up=True)),
            positive_review_ratio=Case(
                When(total_reviews__gt=0, 
                     then=F('positive_reviews') * 1.0 / F('total_reviews')),
                default=0.0,
                output_field=FloatField()
            )
        ).filter(
            wishlist_count__gt=0  # Must be in at least one wishlist
        ).order_by('-wishlist_count')[:10]
        
        data = [{
            'game_id': game.game_id,
            'game_name': game.game_name,
            'wishlist_count': game.wishlist_count,
            'rating': round(game.positive_review_ratio * 10, 1),
            'price': float(game.game_price) if game.game_price else 0.0,
            'image_url': game.gameimages_set.first().image_url if game.gameimages_set.exists() else None
        } for game in games]
        
        return Response(data)
