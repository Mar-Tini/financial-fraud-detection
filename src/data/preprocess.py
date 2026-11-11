from pathlib import Path
import joblib # type: ignore 
import pandas as pd # type: ignore 
from sklearn.preprocessing import OneHotEncoder # type: ignore 


def create_category(df: pd.DataFrame,encoder: OneHotEncoder | None = None):
    if encoder is None:
        encoder = OneHotEncoder(
            drop="first",
            handle_unknown="ignore",
            sparse_output=False
        )

        encoded = encoder.fit_transform(df[["type"]])

    else:
        encoded = encoder.transform(df[["type"]])

    encoded_columns = encoder.get_feature_names_out(["type"])

    encoded_df = pd.DataFrame(
        encoded,
        columns=encoded_columns,
        index=df.index
    )

    df = df.drop(columns=["type"])

    df = pd.concat(
        [df, encoded_df],
        axis=1
    )

    return df, encoder

def split_data(df: pd.DataFrame, train_ratio: float = 0.70,validation_ratio: float = 0.15) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    if not 0 < train_ratio < 1:
        raise ValueError("train_ratio must be between 0 and 1.")

    if not 0 < validation_ratio < 1:
        raise ValueError("validation_ratio must be between 0 and 1.")

    if train_ratio + validation_ratio >= 1:
        raise ValueError("The sum of ratios must be less than 1.")

    if "step" not in df.columns:
        raise ValueError("The 'step' column is missing.")

    # -- Sort chronologically --
    df = df.sort_values("step").reset_index(drop=True)

    max_step = df["step"].max()

    train_end = int(max_step * train_ratio)
    validation_end = int(max_step * (train_ratio + validation_ratio))

    # -- Temporal split --
    train_data = df[df["step"] <= train_end].copy()

    validation_data = df[(df["step"] > train_end) & (df["step"] <= validation_end)].copy()

    test_data = df[df["step"] > validation_end].copy()

    return train_data, validation_data, test_data

def save_split(train_data: pd.DataFrame, validation_data: pd.DataFrame, test_data: pd.DataFrame,data_config: dict) -> None:

    splits = {
        "train": train_data,
        "validation": validation_data,
        "test": test_data
    }

    for split_name, split_df in splits.items():

        output_path = Path(data_config["processed"][split_name])

        output_path.parent.mkdir(parents=True, exist_ok=True)

        split_df.to_parquet(output_path,index=False)

        print(f"# -- {split_name}: {split_df.shape} --")


def preprocessing_data(df: pd.DataFrame, data_config: dict):

    # -- Sort before encoding and splitting --

    df = df.sort_values("step").reset_index(drop=True)

    # -- Create categorical features --
    df, encoder = create_category(df)

    # -- Temporal split --
    train_data, validation_data, test_data = split_data(df)

    # -- Save splits --

    save_split(train_data, validation_data, test_data, data_config)

    return train_data, validation_data, test_data, encoder


def save_preprocessor(preprocessor,preprocessor_path: str):

    output_path = Path(preprocessor_path)

    output_path.parent.mkdir(parents=True,exist_ok=True)

    joblib.dump(preprocessor,output_path)

    print(f"# -- Preprocessor saved to: {output_path} --")