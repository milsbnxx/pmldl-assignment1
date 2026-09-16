from pathlib import Path
import json

import pandas as pd
from sklearn.model_selection import train_test_split


ROOT = Path(__file__).resolve().parents[2]

RAW_PATH = ROOT / "data" / "raw" / "breast_cancer.csv"

PROCESSED_DIR = ROOT / "data" / "processed"
TRAIN_PATH = PROCESSED_DIR / "train.csv"
TEST_PATH = PROCESSED_DIR / "test.csv"
REPORT_PATH = PROCESSED_DIR / "data_report.json"

TARGET = "target"


def remove_iqr_outliers(
    df: pd.DataFrame,
    feature_columns: list[str],
    iqr_multiplier: float = 3.0,
) -> pd.DataFrame:
    """
    Remove only extreme outliers.

    We use 3 * IQR instead of 1.5 * IQR so that we do not remove
    too many valid observations from this relatively small dataset.
    """

    mask = pd.Series(True, index=df.index)

    for column in feature_columns:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)

        iqr = q3 - q1

        if iqr == 0:
            continue

        lower_bound = q1 - iqr_multiplier * iqr
        upper_bound = q3 + iqr_multiplier * iqr

        mask &= df[column].between(
            lower_bound,
            upper_bound,
        )

    return df.loc[mask].copy()


def main() -> None:
    if not RAW_PATH.exists():
        raise FileNotFoundError(
            f"Raw dataset not found: {RAW_PATH}"
        )

    df = pd.read_csv(RAW_PATH)

    if TARGET not in df.columns:
        raise ValueError(
            f"Target column '{TARGET}' was not found."
        )

    feature_columns = [
        column
        for column in df.columns
        if column != TARGET
    ]

    original_rows = len(df)

    # -----------------------------
    # Missing values
    # -----------------------------

    for column in feature_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

        df[column] = df[column].fillna(
            df[column].median()
        )

    df[TARGET] = pd.to_numeric(
        df[TARGET],
        errors="coerce",
    )

    df = df.dropna(
        subset=[TARGET]
    )

    df[TARGET] = df[TARGET].astype(int)

    # -----------------------------
    # Outlier removal
    # -----------------------------

    cleaned_df = remove_iqr_outliers(
        df=df,
        feature_columns=feature_columns,
        iqr_multiplier=3.0,
    )

    if cleaned_df[TARGET].nunique() < 2:
        raise ValueError(
            "Only one target class remained after cleaning."
        )

    # -----------------------------
    # Train / test split
    # -----------------------------

    train_df, test_df = train_test_split(
        cleaned_df,
        test_size=0.20,
        random_state=42,
        stratify=cleaned_df[TARGET],
    )

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    train_df.to_csv(
        TRAIN_PATH,
        index=False,
    )

    test_df.to_csv(
        TEST_PATH,
        index=False,
    )

    # -----------------------------
    # Data report
    # -----------------------------

    report = {
        "raw_rows": int(original_rows),
        "clean_rows": int(len(cleaned_df)),
        "removed_rows": int(
            original_rows - len(cleaned_df)
        ),
        "train_rows": int(len(train_df)),
        "test_rows": int(len(test_df)),
        "number_of_features": int(
            len(feature_columns)
        ),
        "iqr_multiplier": 3.0,
        "target_distribution_train": {
            str(key): int(value)
            for key, value
            in train_df[TARGET]
            .value_counts()
            .sort_index()
            .items()
        },
        "target_distribution_test": {
            str(key): int(value)
            for key, value
            in test_df[TARGET]
            .value_counts()
            .sort_index()
            .items()
        },
    }

    REPORT_PATH.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print("DATA ENGINEERING COMPLETED")
    print("--------------------------")

    print(
        f"Raw rows:     {original_rows}"
    )

    print(
        f"Clean rows:   {len(cleaned_df)}"
    )

    print(
        f"Removed rows: {original_rows - len(cleaned_df)}"
    )

    print(
        f"Train rows:   {len(train_df)}"
    )

    print(
        f"Test rows:    {len(test_df)}"
    )

    print(
        f"Features:     {len(feature_columns)}"
    )

    print()
    print(
        f"Saved train data: {TRAIN_PATH}"
    )

    print(
        f"Saved test data:  {TEST_PATH}"
    )

    print(
        f"Saved report:     {REPORT_PATH}"
    )


if __name__ == "__main__":
    main()