# -- Save Feature Engineering --
import joblib # type: ignore
from pathlib import Path
from src.features.engineering import FraudFeatureEngineer

def save_feature_engineer(feature_engineer: FraudFeatureEngineer,output_path: str):

    path = Path(output_path)

    # -- Create directory if it does not exist --
    path.parent.mkdir(parents=True, exist_ok=True)

    # -- Save transformer --
    joblib.dump(feature_engineer, path, compress=3)

    print(f"# -- Feature Engineering saved to: {path} --")

