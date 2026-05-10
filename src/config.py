from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
DEPLOY_DATA_DIR = DATA_DIR / "deploy"

MODEL_DIR = BASE_DIR / "models"

# Deploy-ready lightweight datasets
MOVIES_PATH = DEPLOY_DATA_DIR / "movies_sample.csv"
RATINGS_PATH = DEPLOY_DATA_DIR / "ratings_sample.csv"

# Processed deploy-ready model data
MODEL_DF_PATH = DEPLOY_DATA_DIR / "model_df.csv"
MOVIE_FEATURES_PATH = DEPLOY_DATA_DIR / "movie_features.csv"

# Model path
XGB_MODEL_PATH = MODEL_DIR / "xgb_model.pkl"