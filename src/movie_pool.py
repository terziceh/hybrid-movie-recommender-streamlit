import pandas as pd


def create_movie_pool(movie_df, selected_genres, min_rating_count=25):
    if not selected_genres:
        return pd.DataFrame()

    filtered = movie_df.copy()

    genre_pattern = "|".join(selected_genres)

    filtered = filtered[
        filtered["genres"].str.contains(
            genre_pattern,
            case=False,
            na=False,
            regex=True,
        )
    ]

    filtered = filtered[filtered["rating_count"] >= min_rating_count]

    filtered = filtered.sort_values(
        by=["avg_rating", "rating_count"],
        ascending=False,
    )

    return filtered


def get_random_movies(movie_pool, n=5):
    if movie_pool.empty:
        return pd.DataFrame()

    sample_size = min(n, len(movie_pool))

    return movie_pool.sample(
        n=sample_size,
        random_state=None,
    )