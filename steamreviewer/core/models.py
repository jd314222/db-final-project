from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Genres(models.Model):
    genre_id = models.AutoField(primary_key=True, db_column='GenreID')
    genre_name = models.CharField(max_length=100, db_column='GenreName')
    
    class Meta:
        db_table = 'Genres'
        verbose_name_plural = 'Genres'
    
    def __str__(self):
        return self.genre_name


class Developers(models.Model):
    developer_id = models.AutoField(primary_key=True, db_column='DeveloperID')
    developer_name = models.CharField(max_length=255, db_column='DeveloperName')
    
    class Meta:
        db_table = 'Developers'
        verbose_name_plural = 'Developers'
    
    def __str__(self):
        return self.developer_name


class Games(models.Model):
    game_id = models.AutoField(primary_key=True, db_column='GameID')
    game_name = models.CharField(max_length=255, db_column='GameName')
    genre = models.ForeignKey(Genres, on_delete=models.SET_NULL, null=True, db_column='GenreID')
    game_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='GamePrice')
    release_year = models.IntegerField(null=True, blank=True, db_column='ReleaseYear')
    storage_gb = models.FloatField(null=True, blank=True, db_column='StorageGB')
    
    class Meta:
        db_table = 'Games'
        verbose_name_plural = 'Games'
        indexes = [
            models.Index(fields=['game_name']),
            models.Index(fields=['genre']),
        ]
    
    def __str__(self):
        return self.game_name


class GameSystemRequirements(models.Model):
    game = models.OneToOneField(Games, on_delete=models.CASCADE, primary_key=True, db_column='GameID')
    cpu_requirements = models.CharField(max_length=255, null=True, blank=True, db_column='CPURequirements')
    gpu_requirements = models.CharField(max_length=255, null=True, blank=True, db_column='GPURequirements')
    ram_requirements = models.CharField(max_length=255, null=True, blank=True, db_column='RAMRequirements')
    
    class Meta:
        db_table = 'GameSystemRequirements'
    
    def __str__(self):
        return f"System Requirements for {self.game.game_name}"


class Users(models.Model):
    user_id = models.AutoField(primary_key=True, db_column='UserID')
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='Budget')
    
    class Meta:
        db_table = 'Users'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"User {self.user_id}"


class UserSpecs(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True, db_column='UserID')
    cpu = models.CharField(max_length=255, null=True, blank=True, db_column='CPU')
    gpu = models.CharField(max_length=255, null=True, blank=True, db_column='GPU')
    ram = models.CharField(max_length=100, null=True, blank=True, db_column='RAM')
    
    class Meta:
        db_table = 'UserSpecs'
        verbose_name_plural = 'User Specs'
    
    def __str__(self):
        return f"Specs for User {self.user.user_id}"


class UserWishList(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='UserID')
    game = models.ForeignKey(Games, on_delete=models.CASCADE, db_column='GameID')
    
    class Meta:
        db_table = 'UserWishList'
        verbose_name_plural = 'User Wish Lists'
        unique_together = ('user', 'game')
    
    def __str__(self):
        return f"User {self.user.user_id} - {self.game.game_name}"


class UserFavoritedGenres(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='UserID')
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE, db_column='GenreID')
    
    class Meta:
        db_table = 'UserFavoritedGenres'
        verbose_name_plural = 'User Favorited Genres'
        unique_together = ('user', 'genre')
    
    def __str__(self):
        return f"User {self.user.user_id} likes {self.genre.genre_name}"


class CreatedGames(models.Model):
    developer = models.ForeignKey(Developers, on_delete=models.CASCADE, db_column='DeveloperID')
    game = models.ForeignKey(Games, on_delete=models.CASCADE, db_column='GameID')
    date_created = models.DateField(db_column='DateCreated')
    
    class Meta:
        db_table = 'CreatedGames'
        verbose_name_plural = 'Created Games'
        unique_together = ('developer', 'game')
    
    def __str__(self):
        return f"{self.developer.developer_name} created {self.game.game_name}"


class Reviews(models.Model):
    review_id = models.AutoField(primary_key=True, db_column='ReviewID')
    game = models.ForeignKey(Games, on_delete=models.CASCADE, db_column='GameID')
    review_text = models.TextField(db_column='ReviewText')
    word_count = models.IntegerField(null=True, blank=True, db_column='WordCount')
    voted_up = models.BooleanField(null=True, blank=True, db_column='VotedUp')
    votes_up = models.IntegerField(default=0, db_column='VotesUp')
    votes_funny = models.IntegerField(default=0, db_column='VotesFunny')
    author_playtime_forever = models.IntegerField(null=True, blank=True, db_column='AuthorPlaytimeForever')
    created_at = models.DateTimeField(db_column='CreatedAt')
    
    class Meta:
        db_table = 'Reviews'
        verbose_name_plural = 'Reviews'
        indexes = [
            models.Index(fields=['game']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"Review {self.review_id} for {self.game.game_name}"


class UserLibrary(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='UserID')
    game = models.ForeignKey(Games, on_delete=models.CASCADE, db_column='GameID')
    purchase_date = models.DateField(db_column='PurchaseDate')
    price_paid = models.DecimalField(max_digits=10, decimal_places=2, db_column='PricePaid')
    
    class Meta:
        db_table = 'userLibrary'
        verbose_name_plural = 'User Libraries'
        unique_together = ('user', 'game')
    
    def __str__(self):
        return f"User {self.user.user_id} owns {self.game.game_name}"


class Tags(models.Model):
    tag_id = models.AutoField(primary_key=True, db_column='TagID')
    tag_string = models.CharField(max_length=255, db_column='TagString')
    
    class Meta:
        db_table = 'Tags'
        verbose_name_plural = 'Tags'
    
    def __str__(self):
        return self.tag_string


class GameTags(models.Model):
    game = models.ForeignKey(Games, on_delete=models.CASCADE, db_column='GameID')
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, db_column='TagID')
    
    class Meta:
        db_table = 'gameTags'
        verbose_name_plural = 'Game Tags'
        unique_together = ('game', 'tag')
    
    def __str__(self):
        return f"{self.game.game_name} - {self.tag.tag_string}"


class GameUrls(models.Model):
    game = models.OneToOneField(Games, on_delete=models.CASCADE, primary_key=True, db_column='GameID')
    url = models.CharField(max_length=500, db_column='URL')
    
    class Meta:
        db_table = 'gameUrls'
        verbose_name_plural = 'Game URLs'
    
    def __str__(self):
        return f"URL for {self.game.game_name}"


class Languages(models.Model):
    game = models.ForeignKey(Games, on_delete=models.CASCADE, db_column='GameID')
    language_supported = models.CharField(max_length=255, db_column='LanguageSupported')
    
    class Meta:
        db_table = 'Languages'
        verbose_name_plural = 'Languages'
        unique_together = ('game', 'language_supported')
    
    def __str__(self):
        return f"{self.game.game_name} - {self.language_supported}"


class GameImages(models.Model):
    game = models.ForeignKey(Games, on_delete=models.CASCADE, db_column='GameID')
    image_url = models.CharField(max_length=500, db_column='ImageURL')
    
    class Meta:
        db_table = 'gameImages'
        verbose_name_plural = 'Game Images'
        unique_together = ('game', 'image_url')
    
    def __str__(self):
        return f"Image for {self.game.game_name}"


class Platform(models.Model):
    plat_id = models.AutoField(primary_key=True, db_column='PlatID')
    platform_name = models.CharField(max_length=255, db_column='PlatformName')
    
    class Meta:
        db_table = 'Platform'
        verbose_name_plural = 'Platforms'
    
    def __str__(self):
        return self.platform_name


class GamePlatform(models.Model):
    game = models.ForeignKey(Games, on_delete=models.CASCADE, db_column='GameID')
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, db_column='PlatID')
    
    class Meta:
        db_table = 'gamePlatform'
        verbose_name_plural = 'Game Platforms'
        unique_together = ('game', 'platform')
    
    def __str__(self):
        return f"{self.game.game_name} on {self.platform.platform_name}"


class Publishers(models.Model):
    pub_id = models.AutoField(primary_key=True, db_column='PubID')
    publisher = models.CharField(max_length=255, db_column='Publisher')
    
    class Meta:
        db_table = 'Publishers'
        verbose_name_plural = 'Publishers'
    
    def __str__(self):
        return self.publisher


class GamePublishers(models.Model):
    game = models.ForeignKey(Games, on_delete=models.CASCADE, db_column='GameID')
    publisher = models.ForeignKey(Publishers, on_delete=models.CASCADE, db_column='PubID')
    publish_date = models.DateField(db_column='PublishDate')
    
    class Meta:
        db_table = 'gamePublishers'
        verbose_name_plural = 'Game Publishers'
        unique_together = ('game', 'publisher')
    
    def __str__(self):
        return f"{self.game.game_name} published by {self.publisher.publisher}"
