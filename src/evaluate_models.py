import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from models.xgb_model import train_xgb_model
from models.svd_model import SVDRecommender


DATA_PATH = ROOT_DIR / "data" / "processed" / "model_df.csv"
RANDOM_STATE = 42


def print_scores(name, y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    print(f"\n{name}")
    print("-" * 40)
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE:  {mae:.4f}")
    print(f"R2:   {r2:.4f}")


def main():
    model_df = pd.read_csv(DATA_PATH)

    train_df, test_df = train_test_split(
        model_df,
        test_size=0.2,
        random_state=RANDOM_STATE,
    )

    # XGBoost
    xgb_model = train_xgb_model(train_df)

    X_test = test_df.drop(
        columns=["rating", "movieId", "userId", "title", "genre_list"],
        errors="ignore",
    )

    y_test = test_df["rating"]

    xgb_preds = xgb_model.predict(X_test)
    xgb_preds = np.clip(xgb_preds, 0.5, 5.0)

    print_scores("XGBoost", y_test, xgb_preds)

    # SVD
    svd_model = SVDRecommender(n_components=50)
    svd_model.fit(train_df[["userId", "movieId", "rating"]])

    svd_preds = [
        svd_model.predict(row.userId, row.movieId)
        for row in test_df.itertuples(index=False)
    ]

    print_scores("SVD", y_test, svd_preds)

    # Hybrid
    hybrid_preds = (0.75 * np.array(svd_preds)) + (0.25 * np.array(xgb_preds))
    hybrid_preds = np.clip(hybrid_preds, 0.5, 5.0)

    print_scores("Hybrid", y_test, hybrid_preds)


if __name__ == "__main__":
    main()