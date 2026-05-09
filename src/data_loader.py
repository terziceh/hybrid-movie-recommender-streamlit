import pandas as pd
import streamlit as st

from src.config import (
    MOVIES_PATH,
    RATINGS_PATH,
    MODEL_DF_PATH,
)


N_USERS = 1000
RANDOM_STATE = 42


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

    n_users = min(N_USERS, ratings["userId"].nunique())

    sample_users = (
        ratings["userId"]
        .drop_duplicates()
        .sample(n=n_users, random_state=RANDOM_STATE)
    )

    ratings_sample = ratings[ratings["userId"].isin(sample_users)].copy()

    df = ratings_sample.merge(
        movies,
        on="movieId",
        how="left",
    )

    genre_dummies = df["genres"].str.get_dummies(sep="|")

    genre_dummies = genre_dummies.drop(
        columns=["(no genres listed)", "IMAX"],
        errors="ignore",
    )

    model_df = pd.concat(
        [
            df[["userId", "movieId", "rating", "title"]],
            genre_dummies,
        ],
        axis=1,
    )

    model_df["genre_list"] = df["genres"]

    MODEL_DF_PATH.parent.mkdir(parents=True, exist_ok=True)
    model_df.to_csv(MODEL_DF_PATH, index=False)

    return model_df