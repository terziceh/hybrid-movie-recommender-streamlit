import pandas as pd
from pathlib import Path

DEPLOY_DIR = Path("data/deploy")
DEPLOY_DIR.mkdir(parents=True, exist_ok=True)

RATINGS_PATH = DEPLOY_DIR / "ratings_sample.csv"
MOVIES_PATH = DEPLOY_DIR / "movies_sample.csv"
MODEL_DF_PATH = DEPLOY_DIR / "model_df.csv"

ratings = pd.read_csv(RATINGS_PATH)
movies = pd.read_csv(MOVIES_PATH)

df = ratings.merge(
    movies,
    on="movieId",
    how="left",
)

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

model_df.to_csv(MODEL_DF_PATH, index=False)

print("Built data/deploy/model_df.csv")
print(f"Users: {ratings['userId'].nunique():,}")
print(f"Rows: {len(model_df):,}")
print(model_df.shape)
print(model_df.columns.tolist())