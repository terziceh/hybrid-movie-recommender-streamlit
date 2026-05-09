import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD


class SVDRecommender:
    def __init__(self, n_components=50, random_state=42):
        self.n_components = n_components
        self.random_state = random_state
        self.model = TruncatedSVD(
            n_components=n_components,
            random_state=random_state,
        )
        self.user_map = {}
        self.movie_map = {}
        self.reverse_movie_map = {}
        self.user_factors = None
        self.movie_factors = None
        self.global_mean = 3.5

    def fit(self, ratings_df):
        ratings_df = ratings_df[["userId", "movieId", "rating"]].copy()

        self.global_mean = ratings_df["rating"].mean()

        users = ratings_df["userId"].unique()
        movies = ratings_df["movieId"].unique()

        self.user_map = {user_id: idx for idx, user_id in enumerate(users)}
        self.movie_map = {movie_id: idx for idx, movie_id in enumerate(movies)}
        self.reverse_movie_map = {idx: movie_id for movie_id, idx in self.movie_map.items()}

        row = ratings_df["userId"].map(self.user_map)
        col = ratings_df["movieId"].map(self.movie_map)
        data = ratings_df["rating"] - self.global_mean

        rating_matrix = csr_matrix(
            (data, (row, col)),
            shape=(len(users), len(movies)),
        )

        self.user_factors = self.model.fit_transform(rating_matrix)
        self.movie_factors = self.model.components_.T

        return self

    def predict(self, user_id, movie_id):
        if user_id not in self.user_map or movie_id not in self.movie_map:
            return float(self.global_mean)

        user_idx = self.user_map[user_id]
        movie_idx = self.movie_map[movie_id]

        score = (
            np.dot(
                self.user_factors[user_idx],
                self.movie_factors[movie_idx],
            )
            + self.global_mean
        )

        return float(np.clip(score, 0.5, 5.0))


def train_svd_model(model_df):
    ratings_df = model_df[["userId", "movieId", "rating"]].copy()
    svd_model = SVDRecommender(n_components=50)
    svd_model.fit(ratings_df)
    return svd_model


def train_svd_with_new_user(model_df, demo_ratings):
    ratings_df = model_df[["userId", "movieId", "rating"]].copy()

    augmented = pd.concat(
        [ratings_df, demo_ratings[["userId", "movieId", "rating"]]],
        ignore_index=True,
    )

    svd_model = SVDRecommender(n_components=50)
    svd_model.fit(augmented)

    return svd_model