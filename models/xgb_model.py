import os
import joblib
import numpy as np
import pandas as pd
from xgboost import XGBRegressor

MODEL_PATH = "models/xgb_model.pkl"

DROP_COLS = ["rating", "movieId", "userId", "title", "genre_list"]


def build_xgb_features(model_df: pd.DataFrame):
    X = model_df.drop(columns=DROP_COLS, errors="ignore")
    y = model_df["rating"]
    return X, y


def train_xgb_model(model_df: pd.DataFrame):
    X, y = build_xgb_features(model_df)

    model = XGBRegressor(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        objective="reg:squarederror",
    )

    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return model


def load_xgb_model(model_df: pd.DataFrame):
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)

    return train_xgb_model(model_df)


def predict_xgb_score(xgb_model, movie_row: pd.DataFrame):
    X = movie_row.drop(columns=DROP_COLS, errors="ignore")
    score = xgb_model.predict(X)[0]
    return float(np.clip(score, 0.5, 5.0))