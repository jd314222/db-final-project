# Steam Reviewer - Setup Guide

**Team:** Ethan Eisnaugle, Patrick McConnell, Jayden Dowell  
**Course:** CS3620 Databases Final Project

## Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already done)
pip install -r requirements.txt

# Navigate to project
cd steamreviewer

# Run migrations
python manage.py migrate

# Download datasets from Kaggle (first time only)
python download_dataset.py

# Import data from CSVs
python manage.py import_data

# Create admin user (if needed)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Visit: http://localhost:8000/admin/

## Project Structure

```
db-final-project/
├── data/                       # CSV datasets
│   ├── pc_videogame_requirements.csv
│   └── steam_game_reviews.csv
├── steamreviewer/              # Django project
│   ├── steamreviewer/         # Settings & config
│   ├── core/               # Models, admin, views
│   └── manage.py
├── venv/                   # Virtual environment
└── requirements.txt
```

## Database Models

- **Games** - Game details with prices and system requirements
- **Reviews** - User reviews with ratings and playtime
- **Genres** - Game categories
- **Developers** - Game developers
- **Users** - User profiles with budgets and specs

## Useful Commands

```bash
python download_dataset.py         # Download datasets from Kaggle
python manage.py runserver         # Start server (localhost:8000)
python manage.py import_data       # Import CSV data
python manage.py shell             # Django shell for queries
python manage.py migrate           # Apply database changes
```

## Querying Data

```python
# In Django shell (python manage.py shell)
from core.models import Games, Reviews

# Get all games
Games.objects.all()

# Search by name
Games.objects.filter(game_name__icontains="Counter")

# Get reviews for a game
Reviews.objects.filter(game__game_name="Cyberpunk 2077")

# Complex queries
from django.db.models import Avg, Count
Games.objects.annotate(
    avg_rating=Avg('reviews__votes_up'),
    review_count=Count('reviews')
).order_by('-review_count')[:10]
```
