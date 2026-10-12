import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from movies.models import Movie
from movies.services import fetch_poster_path


class Command(BaseCommand):
    help = "OPTIONAL: download poster paths for the most popular movies using a free TMDB API key"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=100, help="how many movies (default 100)")

    def handle(self, *args, **options):
        if not settings.TMDB_API_KEY:
            raise CommandError("TMDB_API_KEY is not set. See README.md, section 'Posters'.")
        movies = Movie.objects.filter(poster_path="").order_by("-popularity")[: options["limit"]]
        found = 0
        for movie in movies:
            if fetch_poster_path(movie):
                found += 1
            time.sleep(0.1)  # be polite to the free API
        self.stdout.write(self.style.SUCCESS(f"Posters saved for {found} movies."))
