"""
RECOMMENDATION ENGINE  (Content-Based Filtering)

This file has NO Django code, only scikit-learn. So it is easy to read and explain.

Idea:
  1. TF-IDF turns every movie's 'tags' text into a list of numbers (a vector).
  2. Cosine similarity measures the angle between two vectors.
        score 1.0  -> exactly same content
        score 0.0  -> nothing in common
  3. The movies with the highest scores are the recommendations.
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    def __init__(self, movie_ids, tags):
        """
        movie_ids : list of movie ids
        tags      : list of 'tags' strings (same order as movie_ids)
        """
        self.movie_ids = list(movie_ids)
        # position of every movie id in the matrix, for quick lookup
        self.position = {movie_id: i for i, movie_id in enumerate(self.movie_ids)}

        # TF-IDF: stop_words="english" removes useless words like "the", "is", "and"
        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=10000)
        # Rows = movies, Columns = words, Values = TF-IDF weight
        self.tfidf_matrix = self.vectorizer.fit_transform(tags)

    def has_movie(self, movie_id):
        return movie_id in self.position

    def similar_to(self, movie_id, top_n=10):
        """Return a list of (movie_id, similarity_score), best match first."""
        if movie_id not in self.position:
            return []
        index = self.position[movie_id]

        # Similarity of this ONE movie against ALL movies (a single row, not a huge NxN table,
        # so memory use stays small even for large datasets)
        scores = cosine_similarity(self.tfidf_matrix[index], self.tfidf_matrix).ravel()
        scores[index] = -1  # a movie should not recommend itself

        best_indexes = np.argsort(scores)[::-1][:top_n]  # highest scores first
        return [
            (self.movie_ids[i], float(scores[i]))
            for i in best_indexes
            if scores[i] > 0  # ignore movies with nothing in common
        ]
