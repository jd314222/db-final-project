"""
Django management command to import CSV data into the database.
Usage: python manage.py import_data
"""
from django.core.management.base import BaseCommand
import csv
import os
from core.models import Games, GameSystemRequirements, Genres, Reviews
from datetime import datetime


class Command(BaseCommand):
    help = 'Import data from CSV files into the database'

    def handle(self, *args, **options):
        data_dir = os.path.join(os.path.dirname(__file__), '../../../../data')
        
        self.stdout.write('Starting data import...\n')
        
        # Import game system requirements from PC videogame requirements CSV
        pc_requirements_file = os.path.join(data_dir, 'pc_videogame_requirements.csv')
        if os.path.exists(pc_requirements_file):
            self.import_pc_requirements(pc_requirements_file)
        else:
            self.stdout.write(self.style.WARNING(f'PC requirements file not found: {pc_requirements_file}'))
        
        # Import reviews from the reviews CSV (includes game prices)
        reviews_file = os.path.join(data_dir, 'steam_game_reviews.csv')
        if os.path.exists(reviews_file):
            self.import_reviews(reviews_file)
        else:
            self.stdout.write(self.style.WARNING(f'Reviews file not found: {reviews_file}'))
            self.stdout.write('Skipping review import. Please ensure your reviews CSV is named steam_game_reviews.csv')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Data import completed!'))

    def import_pc_requirements(self, filepath):
        """Import games and system requirements from PC videogame requirements CSV"""
        if not os.path.exists(filepath):
            self.stdout.write(self.style.ERROR(f'File not found: {filepath}'))
            return
        
        self.stdout.write(f'Importing PC requirements from {filepath}...')
        
        # Create a default genre for now
        default_genre, _ = Genres.objects.get_or_create(
            genre_name='Unknown',
            defaults={'genre_name': 'Unknown'}
        )
        
        imported = 0
        skipped = 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    # Try both column name formats
                    game_name = row.get('name', '').strip() or row.get('Game', '').strip()
                    if not game_name:
                        continue
                    
                    # Remove " System Requirements" suffix if present
                    if game_name.endswith(' System Requirements'):
                        game_name = game_name[:-len(' System Requirements')]
                    
                    # Parse file size (convert to GB if needed)
                    file_size = None
                    file_size_str = row.get('File Size:', '').strip() or row.get('File Size', '').strip()
                    if file_size_str:
                        try:
                            # Handle formats like "50 GB", "5.5GB", "500 MB"
                            import re
                            match = re.search(r'([\d.]+)\s*(GB|MB)', file_size_str, re.IGNORECASE)
                            if match:
                                size = float(match.group(1))
                                unit = match.group(2).upper()
                                file_size = size if unit == 'GB' else size / 1024
                        except:
                            pass
                    
                    # Create or get the game (no price from this CSV)
                    game, created = Games.objects.get_or_create(
                        game_name=game_name,
                        defaults={
                            'genre': default_genre,
                            'game_price': None,
                            'release_year': None,
                            'storage_gb': file_size
                        }
                    )
                    
                    if created:
                        # Create system requirements (try both column name formats)
                        cpu = row.get('CPU:', '').strip() or row.get('CPU', '').strip() or None
                        gpu = row.get('Graphics Card:', '').strip() or row.get('Graphics Card', '').strip() or None
                        ram = row.get('Memory:', '').strip() or row.get('Memory', '').strip() or None
                        
                        GameSystemRequirements.objects.create(
                            game=game,
                            cpu_requirements=cpu,
                            gpu_requirements=gpu,
                            ram_requirements=ram
                        )
                        imported += 1
                        
                        if imported % 50 == 0:
                            self.stdout.write(f'  Imported {imported} games...')
                    else:
                        skipped += 1
                        
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  Error importing {row.get("Game", "unknown")}: {str(e)}'))
                    continue
        
        self.stdout.write(self.style.SUCCESS(f'✓ Imported {imported} games, skipped {skipped} duplicates'))

    def import_games(self, filepath):
        """Import games and system requirements from steam_dataset.csv"""
        if not os.path.exists(filepath):
            self.stdout.write(self.style.ERROR(f'File not found: {filepath}'))
            return
        
        self.stdout.write(f'Importing games from {filepath}...')
        
        # Create a default genre for now
        default_genre, _ = Genres.objects.get_or_create(
            genre_name='Unknown',
            defaults={'genre_name': 'Unknown'}
        )
        
        imported = 0
        skipped = 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    # Parse price - treat SR prices as already in reasonable USD range
                    # Divide by ~3.56 to normalize to USD gaming prices
                    price_str = row.get('Price', '').strip()
                    price = None
                    if price_str and price_str != 'No Price':
                        # Extract numeric value from price string
                        # Example: "Your Price:248.95 SR" -> 248.95 -> divide by 3.56 -> ~$69.99
                        import re
                        match = re.search(r'[\d,]+\.?\d*', price_str)
                        if match:
                            price_sr = float(match.group().replace(',', ''))
                            # Normalize SR to typical USD game prices
                            price = round(price_sr / 3.56, 2)
                    
                    # Parse year
                    year_str = row.get('years', '').strip()
                    year = None
                    if year_str and year_str != '0':
                        try:
                            year = int(float(year_str))
                        except:
                            pass
                    
                    # Parse storage
                    storage = None
                    storage_str = row.get('Storage_GB', '').strip()
                    if storage_str:
                        try:
                            storage = float(storage_str)
                        except:
                            pass
                    
                    # Create or get the game
                    game, created = Games.objects.get_or_create(
                        game_name=row['Game Names'].strip(),
                        defaults={
                            'genre': default_genre,
                            'game_price': price,
                            'release_year': year,
                            'storage_gb': storage
                        }
                    )
                    
                    if created:
                        # Create system requirements
                        GameSystemRequirements.objects.create(
                            game=game,
                            cpu_requirements=row.get('Processor_main', '').strip() or None,
                            gpu_requirements=row.get('Graphics', '').strip() or None,
                            ram_requirements=f"{row.get('Memory_GB', '')} GB".strip() if row.get('Memory_GB') else None
                        )
                        imported += 1
                        
                        if imported % 50 == 0:
                            self.stdout.write(f'  Imported {imported} games...')
                    else:
                        skipped += 1
                        
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  Error importing {row.get("Game Names", "unknown")}: {str(e)}'))
                    continue
        
        self.stdout.write(self.style.SUCCESS(f'✓ Imported {imported} games, skipped {skipped} duplicates'))

    def import_reviews(self, filepath):
        """Import reviews from reviews CSV (includes game prices)"""
        if not os.path.exists(filepath):
            self.stdout.write(self.style.ERROR(f'File not found: {filepath}'))
            return
        
        self.stdout.write(f'\nImporting reviews from {filepath}...')
        self.stdout.write('This may take 10-20 minutes for large files...')
        
        imported = 0
        errors = 0
        batch = []
        batch_size = 1000
        
        # Cache games to avoid repeated queries
        game_cache = {}
        default_genre = Genres.objects.get_or_create(genre_name='Unknown')[0]
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    # Find or create the game
                    game_name = row.get('name', '').strip()
                    if not game_name:
                        continue
                    
                    # Parse price from reviews CSV (stored as cents, convert to dollars)
                    price = None
                    price_str = row.get('price', '').strip()
                    if price_str:
                        try:
                            # Prices are stored as cents (6999 = $69.99), divide by 100
                            price = float(price_str) / 100
                        except:
                            pass
                    
                    # Use cache to avoid database hits
                    if game_name not in game_cache:
                        game, created = Games.objects.get_or_create(
                            game_name=game_name,
                            defaults={
                                'genre': default_genre,
                                'game_price': price
                            }
                        )
                        # Update price if game already exists but has no price
                        if not created and price and not game.game_price:
                            game.game_price = price
                            game.save()
                        game_cache[game_name] = game
                    else:
                        game = game_cache[game_name]
                    
                    # Parse timestamp
                    from datetime import datetime
                    timestamp = row.get('timestamp_created', '')
                    created_at = datetime.fromtimestamp(int(timestamp)) if timestamp else datetime.now()
                    
                    # Parse boolean
                    voted_up = row.get('voted_up', '').strip().lower() == 'true'
                    
                    # Add to batch
                    batch.append(Reviews(
                        game=game,
                        review_text=row.get('review', '').strip(),
                        word_count=int(row.get('word_count', 0)) if row.get('word_count') else None,
                        voted_up=voted_up,
                        votes_up=int(row.get('votes_up', 0)) if row.get('votes_up') else 0,
                        votes_funny=int(row.get('votes_funny', 0)) if row.get('votes_funny') else 0,
                        author_playtime_forever=int(row.get('author_playtime_forever', 0)) if row.get('author_playtime_forever') else None,
                        created_at=created_at
                    ))
                    
                    # Bulk insert when batch is full
                    if len(batch) >= batch_size:
                        Reviews.objects.bulk_create(batch)
                        imported += len(batch)
                        batch = []
                        self.stdout.write(f'  Imported {imported} reviews...')
                        
                except Exception as e:
                    errors += 1
                    if errors < 10:  # Only show first 10 errors
                        self.stdout.write(self.style.WARNING(f'  Error: {str(e)}'))
                    continue
            
            # Insert remaining reviews
            if batch:
                Reviews.objects.bulk_create(batch)
                imported += len(batch)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Imported {imported} reviews, {errors} errors'))
