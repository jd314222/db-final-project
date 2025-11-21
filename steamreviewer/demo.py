import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'steamreviewer.settings')
django.setup()

from core.models import Games, Reviews, GameSystemRequirements, Genres
from django.db.models import Count, Avg, Q
from django.db import connection

print("="*60)
print("STEAM GAME DATABASE QUERIES")
print("="*60)

# Show total counts
print(f"\nTotal Games: {Games.objects.count()}")
print(f"Total Reviews: {Reviews.objects.count()}")

# Show most expensive games
print("\n" + "="*60)
print("TOP 5 MOST EXPENSIVE GAMES:")
print("="*60)
for game in Games.objects.filter(game_price__isnull=False).order_by('-game_price')[:5]:
    print(f"  ${game.game_price:>7.2f} - {game.game_name}")

# Show cheapest games
print("\n" + "="*60)
print("TOP 5 CHEAPEST GAMES:")
print("="*60)
for game in Games.objects.filter(game_price__gt=0).order_by('game_price')[:5]:
    print(f"  ${game.game_price:>7.2f} - {game.game_name}")

# Games with most reviews
print("\n" + "="*60)
print("GAMES WITH MOST REVIEWS:")
print("="*60)
for game in Games.objects.annotate(review_count=Count('reviews')).order_by('-review_count')[:5]:
    print(f"  {game.review_count:>6} reviews - {game.game_name}")

# Positive vs Negative reviews
print("\n" + "="*60)
print("REVIEW SENTIMENT ANALYSIS:")
print("="*60)
positive = Reviews.objects.filter(voted_up=True).count()
negative = Reviews.objects.filter(voted_up=False).count()
total = positive + negative
print(f"  Positive Reviews: {positive:>8} ({positive/total*100:.1f}%)")
print(f"  Negative Reviews: {negative:>8} ({negative/total*100:.1f}%)")

# Average price
print("\n" + "="*60)
print("PRICE STATISTICS:")
print("="*60)
price_stats = Games.objects.filter(game_price__isnull=False).aggregate(
    avg_price=Avg('game_price'),
    count=Count('game_id')
)
print(f"  Average Game Price: ${price_stats['avg_price']:.2f}")
print(f"  Games with Prices: {price_stats['count']}")

# Games by release year
print("\n" + "="*60)
print("GAMES BY RELEASE YEAR:")
print("="*60)
year_counts = Games.objects.filter(release_year__isnull=False).values('release_year').annotate(
    count=Count('game_id')
).order_by('-release_year')[:5]
for item in year_counts:
    print(f"  {item['release_year']}: {item['count']} games")

# System requirements sample
print("\n" + "="*60)
print("SAMPLE GAME WITH SYSTEM REQUIREMENTS:")
print("="*60)
game_with_req = Games.objects.filter(
    gamesystemrequirements__isnull=False
).select_related('gamesystemrequirements').first()
if game_with_req:
    print(f"  Game: {game_with_req.game_name}")
    print(f"  Price: ${game_with_req.game_price if game_with_req.game_price else 'N/A'}")
    req = game_with_req.gamesystemrequirements
    print(f"  CPU: {req.cpu_requirements}")
    print(f"  GPU: {req.gpu_requirements}")
    print(f"  RAM: {req.ram_requirements}")

# Games within budget
print("\n" + "="*60)
print("GAMES UNDER $20:")
print("="*60)
budget_games = Games.objects.filter(game_price__lte=20, game_price__gt=0).order_by('game_price')[:5]
for game in budget_games:
    print(f"  ${game.game_price:>6.2f} - {game.game_name}")

# Most helpful reviews
print("\n" + "="*60)
print("MOST HELPFUL REVIEWS:")
print("="*60)
top_reviews = Reviews.objects.order_by('-votes_up')[:3]
for review in top_reviews:
    print(f"\n  Game: {review.game.game_name}")
    print(f"  Rating: {'👍 Positive' if review.voted_up else '👎 Negative'}")
    print(f"  Helpful Votes: {review.votes_up}")
    print(f"  Review: {review.review_text[:100]}...")

print("\n" + "="*60)
print("RAW SQL QUERIES:")
print("="*60)

# Query 1: Top games by average review helpfulness
print("\nTop games by average review helpfulness (SQL):")
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT g.GameName, AVG(r.VotesUp) as avg_helpful, COUNT(r.ReviewID) as review_count
        FROM Games g
        JOIN Reviews r ON g.GameID = r.GameID
        GROUP BY g.GameID, g.GameName
        HAVING COUNT(r.ReviewID) >= 10
        ORDER BY avg_helpful DESC
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]:.1f} avg helpful votes ({row[2]} reviews)")

# Query 2: Price ranges and game counts
print("\nGames by price range (SQL):")
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT 
            CASE 
                WHEN GamePrice < 10 THEN 'Under $10'
                WHEN GamePrice < 30 THEN '$10-$30'
                WHEN GamePrice < 60 THEN '$30-$60'
                ELSE 'Over $60'
            END as price_range,
            COUNT(*) as count
        FROM Games
        WHERE GamePrice IS NOT NULL
        GROUP BY price_range
        ORDER BY MIN(GamePrice)
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} games")


# Query 3: Review word count analysis
print("\nReview length analysis (SQL):")
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT 
            AVG(WordCount) as avg_words,
            MIN(WordCount) as min_words,
            MAX(WordCount) as max_words
        FROM Reviews
        WHERE WordCount IS NOT NULL
    """)
    row = cursor.fetchone()
    print(f"  Average: {row[0]:.0f} words")
    print(f"  Shortest: {row[1]} words")
    print(f"  Longest: {row[2]} words")

print("\n" + "="*60)