import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import numpy as np
import pandas as pd

from models.xgb_model import load_xgb_model, predict_xgb_score
from models.svd_model import train_svd_with_new_user
from src.config import MODEL_DF_PATH

NEW_USER_ID = 999999


def get_title_family(title):
    title = str(title).lower()

    franchises = {
        "lord of the rings": "lord_of_the_rings",
        "star wars": "star_wars",
        "godfather": "godfather",
        "harry potter": "harry_potter",
        "batman": "batman",
        "spider-man": "spiderman",
        "spiderman": "spiderman",
        "avengers": "marvel",
        "iron man": "marvel",
        "captain america": "marvel",
        "x-men": "xmen",
        "toy story": "toy_story",
        "jurassic park": "jurassic_park",
        "jurassic world": "jurassic_park",
    }

    for key, family in franchises.items():
        if key in title:
            return family

    return title.split("(")[0].strip()


def normalize_user_ratings(user_ratings):
    ratings_df = pd.DataFrame(user_ratings)

    if ratings_df.empty:
        return ratings_df

    if "user_rating" in ratings_df.columns and "rating" not in ratings_df.columns:
        ratings_df = ratings_df.rename(columns={"user_rating": "rating"})

    ratings_df["userId"] = NEW_USER_ID

    return ratings_df[["userId", "movieId", "rating"]]


def filter_candidate_movies(movie_stats):
    popular_movies = movie_stats[movie_stats["rating_count"] >= 25]

    if popular_movies.empty:
        popular_movies = movie_stats[movie_stats["rating_count"] >= 5]

    if popular_movies.empty:
        popular_movies = movie_stats.copy()

    return popular_movies


def generate_recommendations(
    movie_df,
    selected_genres,
    user_ratings,
    top_n=5,
):
    if not user_ratings or not selected_genres:
        return pd.DataFrame()

    model_df = pd.read_csv(MODEL_DF_PATH)
    demo_ratings = normalize_user_ratings(user_ratings)

    if demo_ratings.empty:
        return pd.DataFrame()

    rated_movie_ids = set(demo_ratings["movieId"])

    xgb_model = load_xgb_model(model_df)
    svd_model = train_svd_with_new_user(model_df, demo_ratings)

    candidate_df = model_df[~model_df["movieId"].isin(rated_movie_ids)].copy()

    movie_stats = (
        candidate_df
        .groupby(["movieId", "title"])
        .agg(
            avg_rating=("rating", "mean"),
            rating_count=("rating", "count"),
        )
        .reset_index()
    )

    movie_stats = filter_candidate_movies(movie_stats)

    if movie_stats.empty:
        return pd.DataFrame()

    max_rating_count = movie_stats["rating_count"].max()
    predictions = []

    for row in movie_stats.itertuples(index=False):
        movie_rows = model_df[model_df["movieId"] == row.movieId]

        if movie_rows.empty:
            continue

        movie_row = movie_rows.iloc[0]

        genre_match_count = 0

        for genre in selected_genres:
            if genre in model_df.columns:
                genre_match_count += int(movie_row[genre])

        if genre_match_count == 0:
            continue

        genre_score = genre_match_count / len(selected_genres)

        svd_score = svd_model.predict(NEW_USER_ID, row.movieId)

        xgb_score = predict_xgb_score(
            xgb_model=xgb_model,
            movie_row=movie_rows.iloc[0:1],
        )

        popularity_score = np.log1p(row.rating_count) / np.log1p(max_rating_count)

        model_score = (0.65 * svd_score) + (0.20 * xgb_score)

        final_score = (
            model_score
            + (0.25 * genre_score)
            + (0.10 * popularity_score)
        )

        match_percent = int(np.clip((final_score / 5.5) * 100, 60, 98))

        if genre_score >= 0.67:
            reason = f"Strong match with your {', '.join(selected_genres)} preferences."
        elif row.avg_rating >= 4.0:
            reason = "Highly rated by similar movie watchers."
        elif row.rating_count >= 500:
            reason = "Popular pick with a strong rating history."
        else:
            reason = "Balanced recommendation based on your ratings and genre choices."

        confidence = "High" if row.rating_count >= 500 else "Medium"

        predictions.append(
            {
                "movieId": row.movieId,
                "title": row.title,
                "avg_rating": round(row.avg_rating, 2),
                "rating_count": int(row.rating_count),
                "predicted_rating": round(np.clip(model_score, 0.5, 5.0), 2),
                "match_percent": match_percent,
                "final_score": round(final_score, 3),
                "svd_score": round(svd_score, 3),
                "xgb_score": round(xgb_score, 3),
                "genre_score": round(genre_score, 3),
                "popularity_score": round(popularity_score, 3),
                "confidence": confidence,
                "reason": reason,
                "title_family": get_title_family(row.title),
            }
        )

    recs = pd.DataFrame(predictions)

    if recs.empty:
        return pd.DataFrame()

    recs = recs.sort_values("final_score", ascending=False)

    final_recs = []
    family_counts = {}

    for _, row in recs.iterrows():
        family = row["title_family"]

        if family_counts.get(family, 0) < 1:
            final_recs.append(row)
            family_counts[family] = family_counts.get(family, 0) + 1

        if len(final_recs) == top_n:
            break

    return (
        pd.DataFrame(final_recs)
        .drop(columns=["title_family"])
        .reset_index(drop=True)
    )