import pandas as pd
import streamlit as st

from src.config import (
    MOVIES_PATH,
    RATINGS_PATH,
    MODEL_DF_PATH,
)


@st.cache_data
def load_raw_data():
    movies = pd.read_csv(MOVIES_PATH)
    ratings = pd.read_csv(RATINGS_PATH)
    return movies, ratings


@st.cache_data
def build_or_load_model_df(force_rebuild=False):
    if MODEL_DF_PATH.exists() and not force_rebuild:
        return pd.read_csv(MODEL_DF_PATH)

    movies, ratings = load_raw_data()

    # Sample ratings so MVP loads fast
    sample_size = min(250_000, len(ratings))

    ratings_sample = ratings.sample(
        n=sample_size,
        random_state=42,
    )

    df = ratings_sample.merge(
        movies,
        on="movieId",
        how="left",
    )

    movie_stats = (
        df.groupby("movieId")["rating"]
        .agg(
            avg_rating="mean",
            rating_count="count",
        )
        .reset_index()
    )

    movie_features = movies.merge(
        movie_stats,
        on="movieId",
        how="left",
    )

    movie_features["avg_rating"] = movie_features["avg_rating"].fillna(0)
    movie_features["rating_count"] = movie_features["rating_count"].fillna(0)

    # Keep only movies with enough ratings for decent recommendations
    movie_features = movie_features[
        movie_features["rating_count"] >= 20
    ].copy()

    MODEL_DF_PATH.parent.mkdir(parents=True, exist_ok=True)

    movie_features.to_csv(MODEL_DF_PATH, index=False)

    return movie_features