"""
Django management command to import game URLs and images from CSV.
Usage: python manage.py import_game_urls
"""
from django.core.management.base import BaseCommand
from django.db import transaction
import csv
import os
from core.models import Games, GameUrls, GameImages


class Command(BaseCommand):
    help = 'Import game URLs and images from gameid_with_urls.csv'

    def handle(self, *args, **options):
        csv_file = os.path.join(
            os.path.dirname(__file__), 
            '../../../../unimported_data/gameid_with_urls.csv'
        )
        
        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f'CSV file not found: {csv_file}'))
            return
        
        self.stdout.write('Starting game URLs import...\n')
        
        stats = {
            'processed': 0,
            'game_urls_created': 0,
            'game_images_created': 0,
            'skipped_null_images': 0,
            'skipped_no_game_match': 0,
            'errors': 0
        }
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                stats['processed'] += 1
                
                # Extract data from CSV
                game_name = row.get('game_name', '').strip()
                image_url = row.get('image_url', '').strip()
                
                # Skip if image URL is NULL or empty
                if not image_url or image_url.upper() == 'NULL':
                    stats['skipped_null_images'] += 1
                    continue
                
                # Find matching game by name in the database
                try:
                    # Try exact match first
                    game = Games.objects.filter(game_name=game_name).first()
                    
                    if not game:
                        # Try case-insensitive match
                        game = Games.objects.filter(game_name__iexact=game_name).first()
                    
                    if not game:
                        self.stdout.write(
                            self.style.WARNING(
                                f'No matching game found for: {game_name}'
                            )
                        )
                        stats['skipped_no_game_match'] += 1
                        continue
                    
                    # Create or update GameUrls entry
                    # The URL field will store the Steam page URL
                    steam_url = f'https://store.steampowered.com/app/{game.game_id}/'
                    
                    game_url, created = GameUrls.objects.update_or_create(
                        game=game,
                        defaults={'url': steam_url}
                    )
                    
                    if created:
                        stats['game_urls_created'] += 1
                    
                    # Create GameImages entry with the image URL
                    game_image, created = GameImages.objects.get_or_create(
                        game=game,
                        image_url=image_url
                    )
                    
                    if created:
                        stats['game_images_created'] += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ Added image for: {game_name} (Game ID: {game.game_id})'
                            )
                        )
                
                except Exception as e:
                    stats['errors'] += 1
                    self.stdout.write(
                        self.style.ERROR(
                            f'Error processing {game_name}: {str(e)}'
                        )
                    )
        
        # Print summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('Import completed!'))
        self.stdout.write(f"Rows processed: {stats['processed']}")
        self.stdout.write(f"Game URLs created: {stats['game_urls_created']}")
        self.stdout.write(f"Game images created: {stats['game_images_created']}")
        self.stdout.write(f"Skipped (NULL images): {stats['skipped_null_images']}")
        self.stdout.write(f"Skipped (no game match): {stats['skipped_no_game_match']}")
        self.stdout.write(f"Errors: {stats['errors']}")
        self.stdout.write('='*60 + '\n')
