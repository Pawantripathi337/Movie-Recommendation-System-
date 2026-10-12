from django.conf import settings
from django.shortcuts import render

from .models import Movie
from .services import fetch_poster_path, get_similar_movies


def _find_movie(movie_id_text):
    """
    Safely find a movie from the id written in the URL.
    Returns None for invalid ids (like 'abc') and for ids that do not exist.
    """
    try:
        movie_id = int(movie_id_text)
    except (TypeError, ValueError):
        return None
    return Movie.objects.filter(movie_id=movie_id).first()


def _error_page(request, message):
    return render(request, "error.html", {"message": message}, status=404)


def home(request):
    context = {
        "dataset_missing": not Movie.objects.exists(),
        "popular_movies": Movie.objects.order_by("-popularity")[:12],
        "top_rated_movies": Movie.objects.filter(vote_count__gte=1000).order_by("-vote_average")[:12],
    }
    return render(request, "home.html", context)


def search(request):
    query = request.GET.get("q", "").strip()
    results = []
    message = ""
    if not query:
        message = "Please type a movie name to search."
    else:
        results = Movie.objects.filter(title__icontains=query).order_by("-popularity")[:40]
        if not results:
            message = f'No movies found for "{query}". Try a shorter or different name.'
    return render(request, "search.html", {"query": query, "results": results, "message": message})


def movie_detail(request, movie_id):
    movie = _find_movie(movie_id)
    if movie is None:
        return _error_page(request, "Sorry, this movie was not found. The link may be wrong.")
    # Try to get a real poster (only if the free TMDB key is set)
    if not movie.poster_path and settings.TMDB_API_KEY:
        fetch_poster_path(movie)
    recommendations = get_similar_movies(movie, top_n=8)
    return render(request, "movie_detail.html", {"movie": movie, "recommendations": recommendations})


def recommendations(request, movie_id):
    movie = _find_movie(movie_id)
    if movie is None:
        return _error_page(request, "Sorry, this movie was not found. The link may be wrong.")
    recommendations = get_similar_movies(movie, top_n=10)
    return render(request, "recommendations.html", {"movie": movie, "recommendations": recommendations})
