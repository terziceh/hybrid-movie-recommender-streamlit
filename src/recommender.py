import pandas as pd


def generate_recommendations(
    movie_df,
    selected_genres,
    user_ratings,
    top_n=5,
):
    if not user_ratings:
        return pd.DataFrame()

    liked_movies = pd.DataFrame(user_ratings)

    avg_user_rating = liked_movies["user_rating"].mean()

    genre_pattern = "|".join(selected_genres)

    recommendations = movie_df.copy()

    recommendations = recommendations[
        recommendations["genres"].str.contains(
            genre_pattern,
            case=False,
            na=False,
            regex=True,
        )
    ]

    rated_movie_ids = liked_movies["movieId"].tolist()

    recommendations = recommendations[
        ~recommendations["movieId"].isin(rated_movie_ids)
    ]

    recommendations["genre_match_score"] = recommendations["genres"].apply(
        lambda x: sum(
            genre.lower() in x.lower()
            for genre in selected_genres
        )
    )

    recommendations["final_score"] = (
        recommendations["avg_rating"] * 0.6
        + recommendations["genre_match_score"] * 0.3
        + (recommendations["rating_count"] / 1000) * 0.1
    )

    if avg_user_rating >= 4:
        recommendations["final_score"] *= 1.1

    recommendations = recommendations.sort_values(
        by="final_score",
        ascending=False,
    )

    return recommendations.head(top_n)