"""
DATA PREPROCESSING PIPELINE  (uses Pandas)

Input : tmdb_5000_movies.csv + tmdb_5000_credits.csv
Output: a clean table with one row per movie and a combined 'tags' column
"""
import json
from pathlib import Path

import pandas as pd

from .text_utils import build_tags


def parse_names(json_text, limit=None):
    """
    Many TMDB columns contain JSON text like:
        '[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}]'
    This function returns just the names: ["Action", "Adventure"].
    Missing / broken values give an empty list (no crash).
    """
    try:
        items = json.loads(json_text)
    except (TypeError, ValueError):
        return []
    names = [item.get("name", "") for item in items if isinstance(item, dict)]
    return names[:limit] if limit else names


def get_director(crew_json):
    """Find the person whose job is 'Director' in the crew list."""
    try:
        crew = json.loads(crew_json)
    except (TypeError, ValueError):
        return ""
    for person in crew:
        if isinstance(person, dict) and person.get("job") == "Director":
            return person.get("name", "")
    return ""


def preprocess(movies_csv, credits_csv):
    """Run all preprocessing steps and return a clean DataFrame."""
    movies = pd.read_csv(movies_csv)
    credits = pd.read_csv(credits_csv)

    # STEP 1: Merge the two files. credits has 'movie_id', movies has 'id'.
    credits = credits.rename(columns={"movie_id": "id"}).drop(columns=["title"], errors="ignore")
    df = movies.merge(credits, on="id", how="inner")

    # STEP 2: Handle missing values
    df = df.dropna(subset=["title"])            # a movie without a title is useless
    df = df.drop_duplicates(subset=["id"])      # one row per movie
    df["overview"] = df["overview"].fillna("")  # no description -> empty text
    df["vote_average"] = df["vote_average"].fillna(0)
    df["vote_count"] = df["vote_count"].fillna(0).astype(int)
    df["popularity"] = df["popularity"].fillna(0)
    # release_date -> just the year (bad dates become empty)
    df["release_year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year.astype("Int64")

    # STEP 3: Extract useful names from the JSON text columns
    df["genre_list"] = df["genres"].apply(parse_names)
    df["keyword_list"] = df["keywords"].apply(parse_names)
    df["cast_list"] = df["cast"].apply(lambda value: parse_names(value, limit=5))
    df["director"] = df["crew"].apply(get_director)

    # STEP 4 + 5: Build the 'tags' column (lowercase, cleaned, all text combined).
    # Only the top 3 actors are used for tags: they matter most.
    df["tags"] = df.apply(
        lambda row: build_tags(
            row["overview"], row["genre_list"], row["keyword_list"],
            row["cast_list"][:3], row["director"],
        ),
        axis=1,
    )

    # STEP 6: Keep only the columns we need, in readable form for the website
    clean = pd.DataFrame({
        "movie_id": df["id"],
        "title": df["title"],
        "genres": df["genre_list"].apply(", ".join),
        "keywords": df["keyword_list"].apply(", ".join),
        "overview": df["overview"],
        "cast": df["cast_list"].apply(", ".join),
        "director": df["director"],
        "vote_average": df["vote_average"],
        "vote_count": df["vote_count"],
        "release_year": df["release_year"],
        "popularity": df["popularity"],
        "tags": df["tags"],
    })
    return clean.reset_index(drop=True)


def save_processed(clean_df, output_csv):
    Path(output_csv).parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(output_csv, index=False)
