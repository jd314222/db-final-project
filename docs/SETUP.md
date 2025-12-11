# Steam Reviewer - Setup Guide

**Team:** Ethan Eisnaugle, Patrick McConnell, Jayden Dowell  
**Course:** CS3620 Databases Final Project

## Quick Start

### Backend (Django)

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

# Start backend server
python manage.py runserver
```

Backend will run at: http://localhost:8000

### Frontend (Next.js)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Start frontend development server
npm run dev
```

Frontend will run at: http://localhost:3000

Visit the frontend to browse games, create an account, and manage your wishlist!

## Project Structure

```
db-final-project/
├── data/                       # CSV datasets
│   ├── pc_videogame_requirements.csv
│   └── steam_game_reviews.csv
├── steamreviewer/              # Django backend
│   ├── steamreviewer/         # Settings & config
│   ├── core/                  # Models, admin, views, API
│   └── manage.py
├── frontend/                   # Next.js frontend
│   ├── app/                   # Pages (home, games, reviews, profile)
│   ├── components/            # Reusable components (Navigation)
│   └── lib/                   # Utilities (API client, auth)
├── venv/                      # Virtual environment
└── requirements.txt
```

## Features

### User Features
- **Registration**: Create account with budget and system specs
- **Login/Logout**: Simple authentication system
- **Browse Games**: Filter by genre, price, budget, search by name
- **Game Details**: View system requirements, reviews, and ratings
- **Wishlist**: Add/remove games from your personal wishlist
- **User Profile**: View your specs, budget, and manage wishlist

### Database Models
- **Games** - Game details with prices and system requirements
- **Reviews** - User reviews with ratings and playtime
- **Genres** - Game categories
- **Developers** - Game developers
- **Users** - User profiles with budgets and specs
- **UserWishList** - User's wishlisted games
- **UserLibrary** - User's purchased games
- **Tags, Publishers, Platforms** - Additional game metadata

## Useful Commands

### Backend Commands
```bash
python download_dataset.py         # Download datasets from Kaggle
python manage.py runserver         # Start backend server (localhost:8000)
python manage.py import_data       # Import CSV data
python manage.py shell             # Django shell for queries
python manage.py migrate           # Apply database changes
python manage.py createsuperuser   # Create admin user
```

### Frontend Commands
```bash
npm run dev                        # Start frontend dev server (localhost:3000)
npm run build                      # Build for production
npm run start                      # Start production server
```

## API Endpoints

The Django REST API is available at `http://localhost:8000/api/`

- `GET /api/games/` - List all games (with filtering)
- `GET /api/games/{id}/` - Get game details
- `GET /api/reviews/` - List all reviews
- `GET /api/genres/` - List all genres
- `POST /api/users/` - Create new user (registration)
- `GET /api/users/{id}/` - Get user details
- `POST /api/user-specs/` - Create user system specs
- `GET /api/wishlist/?user={id}` - Get user's wishlist
- `POST /api/wishlist/` - Add game to wishlist
- `DELETE /api/wishlist/{user_id}_{game_id}/` - Remove from wishlist

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
