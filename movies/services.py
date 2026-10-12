"""
'Glue' code between Django (database) and the recommendation engine.
Views call these functions so that views.py stays short and simple.
"""
import requests
from django.conf import settings

from .models import Movie
from .recommendation import MovieRecommender

_recommender = None  # cache: the TF-IDF model is built once, then reused


def reset_recommender():
    """Forget the cached model (called automatically when a movie is added/edited/deleted)."""
    global _recommender
    _recommender = None


def get_recommender():
    """Build the TF-IDF model from the database the first time it is needed."""
    global _recommender
    if _recommender is None:
        rows = list(Movie.objects.exclude(tags="").values_list("movie_id", "tags"))
        if not rows:
            return None
        movie_ids, tags = zip(*rows)
        try:
            _recommender = MovieRecommender(movie_ids, tags)
        except ValueError:  # happens if every tag is empty
            return None
    return _recommender


def get_similar_movies(movie, top_n=8):
    """Return a list like [{'movie': <Movie>, 'percent': 63}, ...]. Empty list if none."""
    recommender = get_recommender()
    if recommender is None:
        return []
    pairs = recommender.similar_to(movie.movie_id, top_n=top_n)
    movies_by_id = Movie.objects.in_bulk([movie_id for movie_id, _ in pairs], field_name="movie_id")
    return [
        {"movie": movies_by_id[movie_id], "percent": round(score * 100)}
        for movie_id, score in pairs
        if movie_id in movies_by_id
    ]


def fetch_poster_path(movie):
    """
    Ask TMDB (free API key) for the poster of one movie and save it.
    Returns the poster path, or '' if the key is missing / internet is down / not found.
    This function NEVER crashes the website.
    """
    if not settings.TMDB_API_KEY:
        return ""
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie.movie_id}",
            params={"api_key": settings.TMDB_API_KEY},
            timeout=5,
        )
        response.raise_for_status()
        poster_path = response.json().get("poster_path") or ""
    except (requests.RequestException, ValueError):
        return ""
    if poster_path:
        Movie.objects.filter(pk=movie.pk).update(poster_path=poster_path)
        movie.poster_path = poster_path
    return poster_path
