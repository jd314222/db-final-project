# Minecraft Mob Probability Calculator - Setup Guide

**Team:** Ethan Eisnaugle, Patrick McConnell, Jayden Dowell  
**Course:** CS3620 Databases Final Project

## Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already done)
pip install -r requirements.txt

# Navigate to project
cd blockheads

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Visit: http://localhost:8000/admin/

## Project Structure

```
db-final-project/
├── blockheads/              # Django project
│   ├── blockheads/         # Settings & config
│   ├── core/               # Main app (add models here)
│   └── manage.py
├── venv/                   # Virtual environment
└── requirements.txt
```

## Development Workflow

### 1. Create Models
Edit `blockheads/core/models.py`:
```python
from django.db import models

class Mob(models.Model):
    name = models.CharField(max_length=100)
    health = models.FloatField()
    
    def __str__(self):
        return self.name
```

### 2. Apply Changes
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Register in Admin
Edit `blockheads/core/admin.py`:
```python
from django.contrib import admin
from .models import Mob

admin.site.register(Mob)
```

### 4. Create API (Optional)
Create `blockheads/core/serializers.py`:
```python
from rest_framework import serializers
from .models import Mob

class MobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mob
        fields = '__all__'
```

Update `blockheads/core/views.py`:
```python
from rest_framework import viewsets
from .models import Mob
from .serializers import MobSerializer

class MobViewSet(viewsets.ModelViewSet):
    queryset = Mob.objects.all()
    serializer_class = MobSerializer
```

Update `blockheads/core/urls.py`:
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MobViewSet

router = DefaultRouter()
router.register(r'mobs', MobViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

## Useful Commands

```bash
python manage.py runserver        # Start dev server
python manage.py makemigrations   # Create migrations
python manage.py migrate          # Apply migrations
python manage.py createsuperuser  # Create admin user
python manage.py shell            # Django shell
python manage.py test             # Run tests
```

## Switching to PostgreSQL

```bash
# Install driver
pip install psycopg2-binary

# Create database
createdb minecraft_mob_calc
```

Update `blockheads/blockheads/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'minecraft_mob_calc',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Then run `python manage.py migrate` again.

## What's Included

- Django 4.2.7 + REST Framework
- CORS headers configured
- SQLite database (easy to switch)
- Admin panel ready
- API routing set up

## Endpoints

- Admin: http://localhost:8000/admin/
- API: http://localhost:8000/api/
