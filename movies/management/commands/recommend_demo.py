from django.core.management.base import BaseCommand

from movies.models import Movie
from movies.services import get_similar_movies


class Command(BaseCommand):
    help = 'Test the recommender in the terminal, e.g.  python manage.py recommend_demo "Avatar"'

    def add_arguments(self, parser):
        parser.add_argument("title", type=str)

    def handle(self, *args, **options):
        movie = Movie.objects.filter(title__icontains=options["title"]).first()
        if movie is None:
            self.stdout.write(self.style.ERROR("Movie not found in the database."))
            return
        self.stdout.write(f"\nSelected movie: {movie.title}\nRecommended:")
        results = get_similar_movies(movie, top_n=10)
        if not results:
            self.stdout.write("  (no similar movies found)")
        for number, item in enumerate(results, start=1):
            self.stdout.write(f"  {number}. {item['movie'].title}  (similarity {item['percent']}%)")
