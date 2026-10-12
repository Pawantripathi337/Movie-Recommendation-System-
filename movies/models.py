from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.templatetags.static import static

from .text_utils import build_tags

POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"


def _split(text):
    """'Action, Adventure' -> ['Action', 'Adventure']"""
    return [item.strip() for item in text.split(",") if item.strip()]


class Movie(models.Model):
    movie_id = models.IntegerField(unique=True, help_text="TMDB movie id")
    title = models.CharField(max_length=255)
    genres = models.CharField(max_length=255, blank=True, help_text="Comma separated, e.g. Action, Adventure")
    keywords = models.TextField(blank=True, help_text="Comma separated")
    overview = models.TextField(blank=True)
    cast = models.CharField(max_length=500, blank=True, help_text="Comma separated")
    director = models.CharField(max_length=255, blank=True)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    release_year = models.IntegerField(null=True, blank=True)
    popularity = models.FloatField(default=0)
    poster_path = models.CharField(max_length=255, blank=True)
    tags = models.TextField(blank=True, help_text="Leave empty: it is created automatically")

    class Meta:
        ordering = ["-popularity"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # If a movie is added from the admin panel without tags, create them automatically
        if not self.tags:
            self.tags = build_tags(
                self.overview, _split(self.genres), _split(self.keywords),
                _split(self.cast)[:3], self.director,
            )
        super().save(*args, **kwargs)

    @property
    def poster_url(self):
        """Real poster if we have one, otherwise our placeholder image."""
        if self.poster_path:
            return POSTER_BASE_URL + self.poster_path
        return static("images/no-poster.svg")

    @property
    def genre_list(self):
        return _split(self.genres)

    @property
    def cast_list(self):
        return _split(self.cast)


@receiver([post_save, post_delete], sender=Movie)
def refresh_recommender(sender, **kwargs):
    """When movies change, the cached TF-IDF model must be rebuilt."""
    from .services import reset_recommender
    reset_recommender()
