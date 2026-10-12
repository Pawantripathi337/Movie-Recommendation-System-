import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from movies.models import Movie


class Command(BaseCommand):
    help = "Load data/processed_movies.csv into the SQLite database"

    def handle(self, *args, **options):
        csv_file = settings.DATA_DIR / "processed_movies.csv"
        if not csv_file.exists():
            raise CommandError(
                f"{csv_file} not found. Run this first:  python manage.py preprocess_data"
            )
        df = pd.read_csv(csv_file).fillna("")
        Movie.objects.all().delete()  # start fresh so we never get duplicates

        movie_objects = [
            Movie(
                movie_id=int(row["movie_id"]),
                title=row["title"],
                genres=row["genres"],
                keywords=row["keywords"],
                overview=row["overview"],
                cast=row["cast"],
                director=row["director"],
                vote_average=float(row["vote_average"] or 0),
                vote_count=int(row["vote_count"] or 0),
                release_year=int(row["release_year"]) if row["release_year"] != "" else None,
                popularity=float(row["popularity"] or 0),
                tags=row["tags"],
            )
            for _, row in df.iterrows()
        ]
        Movie.objects.bulk_create(movie_objects, batch_size=500)
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(movie_objects)} movies into the database."))
