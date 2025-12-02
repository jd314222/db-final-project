from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Q, F, Case, When, FloatField
from django_filters.rest_framework import DjangoFilterBackend

from .models import Games, Reviews, Genres, Developers, Users, UserWishList
from .serializers import (
    GamesListSerializer, GamesDetailSerializer, ReviewsSerializer,
    GenresSerializer, DevelopersSerializer, UsersSerializer, UserWishListSerializer
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
    
    Filters: game_id, voted_up (sentiment), ordering by helpfulness
    """
    queryset = Reviews.objects.select_related('game').order_by('-created_at')
    serializer_class = ReviewsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['game']
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
    """API endpoint for user profiles"""
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class UserWishListViewSet(viewsets.ModelViewSet):
    """API endpoint for user wishlists"""
    queryset = UserWishList.objects.select_related('user', 'game')
    serializer_class = UserWishListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']
