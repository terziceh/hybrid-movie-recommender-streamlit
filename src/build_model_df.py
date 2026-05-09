import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

N_USERS = 5000
RANDOM_STATE = 42

ratings = pd.read_csv(RAW_DIR / "ratings.csv")
movies = pd.read_csv(RAW_DIR / "movies.csv")

n_users = min(N_USERS, ratings["userId"].nunique())

sample_users = (
    ratings["userId"]
    .drop_duplicates()
    .sample(n=n_users, random_state=RANDOM_STATE)
)

ratings_sample = ratings[ratings["userId"].isin(sample_users)].copy()

df = ratings_sample.merge(movies, on="movieId", how="left")

genre_dummies = df["genres"].str.get_dummies(sep="|")

genre_dummies = genre_dummies.drop(
    columns=["(no genres listed)", "IMAX"],
    errors="ignore",
)

movie_stats = (
    df.groupby(["movieId", "title", "genres"])
    .agg(
        avg_rating=("rating", "mean"),
        rating_count=("rating", "count"),
    )
    .reset_index()
)

model_df = df[["userId", "movieId", "rating"]].merge(
    movie_stats,
    on="movieId",
    how="left",
)

model_df = pd.concat(
    [
        model_df.reset_index(drop=True),
        genre_dummies.reset_index(drop=True),
    ],
    axis=1,
)

model_df["genre_list"] = model_df["genres"]

model_df.to_csv(PROCESSED_DIR / "model_df.csv", index=False)

print("Built sampled data/processed/model_df.csv")
print(f"Users sampled: {n_users}")
print(f"Rows: {len(model_df):,}")
print(model_df.shape)
print(model_df.columns.tolist())