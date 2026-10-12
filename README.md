# Movie Recommendation System Using Big Data Analysis

Content-based movie recommender: **Django + Pandas + Scikit-learn (TF-IDF + Cosine Similarity) + SQLite**.

## Setup (Windows commands first, Mac/Linux in brackets)

1. Open this folder in VS Code, open the terminal (Ctrl + `).
2. Create virtual environment:  `python -m venv venv`
3. Activate it:  `venv\Scripts\activate`   (Mac/Linux: `source venv/bin/activate`)
4. Install packages:  `pip install -r requirements.txt`
5. Download the dataset (free Kaggle account): search **"TMDB 5000 Movie Dataset"**.
   Put `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` inside the `data/` folder.
6. Clean the data:  `python manage.py preprocess_data`
   (creates `data/processed_movies.csv`)
7. Create database tables:
   `python manage.py makemigrations movies`
   `python manage.py migrate`
8. Load movies into SQLite:  `python manage.py load_movies`
9. (Optional) Test the recommender in the terminal:  `python manage.py recommend_demo "Avatar"`
10. (Optional) Create an admin login:  `python manage.py createsuperuser`
11. Start the server:  `python manage.py runserver`
12. Open  http://127.0.0.1:8000/   (admin panel: http://127.0.0.1:8000/admin/)

## Posters (optional, free)
The dataset has no poster images, so a placeholder is shown by default and everything still works.
For real posters: make a free account on themoviedb.org -> Settings -> API -> copy the "API Key".
Then set it in the same terminal before running the commands:
- Windows: `set TMDB_API_KEY=your_key`      Mac/Linux: `export TMDB_API_KEY=your_key`
- `python manage.py fetch_posters --limit 100`  (saves posters of the 100 most popular movies)
- Any movie you open also fetches its own poster automatically when the key is set.

## How it works
CSV files -> Pandas cleaning (`movies/preprocessing.py`) -> `tags` column -> TF-IDF vectors ->
cosine similarity (`movies/recommendation.py`) -> Django views -> web pages.

## Important files
- `movies/text_utils.py`      lowercase / clean text, build the `tags` string
- `movies/preprocessing.py`   full Pandas preprocessing pipeline
- `movies/recommendation.py`  TF-IDF + cosine similarity (no Django code)
- `movies/services.py`        connects database + recommender (+ optional poster fetch)
- `movies/views.py`           page logic and friendly error handling
- `movies/management/commands/`  preprocess_data, load_movies, fetch_posters, recommend_demo

## Big Data Analysis note
TMDB 5000 is a small dataset (~4,800 movies). This project does not claim to be "big data";
it demonstrates the same pipeline used on large datasets (collection, cleaning, feature extraction,
TF-IDF, similarity, recommendation) and can be scaled to bigger datasets (for example with Apache Spark).
