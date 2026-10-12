from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from movies.preprocessing import preprocess, save_processed


class Command(BaseCommand):
    help = "Clean the TMDB CSV files and create data/processed_movies.csv"

    def handle(self, *args, **options):
        movies_csv = settings.DATA_DIR / "tmdb_5000_movies.csv"
        credits_csv = settings.DATA_DIR / "tmdb_5000_credits.csv"
        for file in (movies_csv, credits_csv):
            if not file.exists():
                raise CommandError(
                    f"Dataset file not found: {file}\n"
                    "Download the 'TMDB 5000 Movie Dataset' from Kaggle and put "
                    "tmdb_5000_movies.csv and tmdb_5000_credits.csv inside the 'data' folder."
                )
        self.stdout.write("Reading and cleaning data... (about 10-20 seconds)")
        clean = preprocess(movies_csv, credits_csv)
        output = settings.DATA_DIR / "processed_movies.csv"
        save_processed(clean, output)
        self.stdout.write(self.style.SUCCESS(f"Done! {len(clean)} movies saved to {output}"))
        self.stdout.write("\nSample 'tags' of the first movie:")
        self.stdout.write(clean.iloc[0]["tags"][:300] + " ...")
