from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODEL_DIR = BASE_DIR / "models"

MOVIES_PATH = RAW_DATA_DIR / "movies.csv"
RATINGS_PATH = RAW_DATA_DIR / "ratings.csv"

MODEL_DF_PATH = PROCESSED_DATA_DIR / "model_df.csv"
MOVIE_FEATURES_PATH = PROCESSED_DATA_DIR / "movie_features.csv"

XGB_MODEL_PATH = MODEL_DIR / "xgb_model.pkl"