import pandas as pd


def create_movie_pool(movie_df, selected_genres, min_rating_count=10):
    if movie_df is None or movie_df.empty:
        return pd.DataFrame()

    if not selected_genres:
        return pd.DataFrame()

    filtered = movie_df.copy()
    selected_genres_lower = [genre.lower() for genre in selected_genres]

    if "genres" in filtered.columns:
        genre_col = "genres"
    elif "genre_list" in filtered.columns:
        genre_col = "genre_list"
    else:
        return pd.DataFrame()

    def count_genre_matches(value):
        if pd.isna(value):
            return 0

        genres_text = str(value).lower()

        return sum(
            selected_genre in genres_text
            for selected_genre in selected_genres_lower
        )

    filtered["genre_match_count"] = filtered[genre_col].apply(count_genre_matches)

    filtered = filtered[filtered["genre_match_count"] > 0].copy()

    if filtered.empty:
        return pd.DataFrame()

    if "movieId" in filtered.columns:
        filtered = filtered.drop_duplicates(
            subset=["movieId"],
            keep="first",
        ).copy()
    elif "title" in filtered.columns:
        filtered = filtered.drop_duplicates(
            subset=["title"],
            keep="first",
        ).copy()

    rating_count_col = None

    if "rating_count" in filtered.columns:
        rating_count_col = "rating_count"
    elif "ratings_count" in filtered.columns:
        rating_count_col = "ratings_count"

    if rating_count_col:
        filtered = filtered[
            filtered[rating_count_col] >= min_rating_count
        ].copy()

    if filtered.empty:
        return pd.DataFrame()

    sort_cols = ["genre_match_count"]
    ascending = [False]

    if "avg_rating" in filtered.columns:
        sort_cols.append("avg_rating")
        ascending.append(False)
    elif "average_rating" in filtered.columns:
        sort_cols.append("average_rating")
        ascending.append(False)

    if rating_count_col:
        sort_cols.append(rating_count_col)
        ascending.append(False)

    filtered = filtered.sort_values(
        by=sort_cols,
        ascending=ascending,
    )

    return filtered.reset_index(drop=True)


def get_random_movies(movie_pool, n=20):
    if movie_pool is None or movie_pool.empty:
        return pd.DataFrame()

    movie_pool = movie_pool.copy()

    if "movieId" in movie_pool.columns:
        movie_pool = movie_pool.drop_duplicates(
            subset=["movieId"],
            keep="first",
        ).copy()
    elif "title" in movie_pool.columns:
        movie_pool = movie_pool.drop_duplicates(
            subset=["title"],
            keep="first",
        ).copy()

    if "genre_match_count" in movie_pool.columns:
        max_match_count = movie_pool["genre_match_count"].max()

        strongest_pool = movie_pool[
            movie_pool["genre_match_count"] == max_match_count
        ].copy()

        if len(strongest_pool) >= n:
            movie_pool = strongest_pool
        else:
            second_best_pool = movie_pool[
                movie_pool["genre_match_count"] >= max(1, max_match_count - 1)
            ].copy()

            if len(second_best_pool) >= n:
                movie_pool = second_best_pool

    sample_size = min(n, len(movie_pool))

    return (
        movie_pool
        .sample(n=sample_size, random_state=None)
        .reset_index(drop=True)
    )