from src.config import load_config
from src.data.load import load_data
from src.features.engineering import feature_data

from src.models.train import train_model
from src.models.evaluate import evaluate_model
from src.models.save import save_model
from src.models.visualisation import visualize_all
from src.models.threshold import find_best_threshold


def run_pipeline():

    # -- Load configuration --
    data_config, model_config = load_config()

    # -- Load data --
    train_data = load_data(data_config["data"]["processed"]["train"])
    validation_data = load_data(data_config["data"]["processed"]["validation"])
    test_data = load_data(data_config["data"]["processed"]["test"])
    
    train_data = train_data[model_config['features']]
    validation_data = validation_data[model_config['features']]
    test_data = test_data[model_config['features']]
    
    # -- Feature engineering --
    X_train, y_train, X_validation, y_validation, X_test, y_test = feature_data(
        train_data,
        validation_data,
        test_data
    )

    print(f"\nTrain shape      : {X_train.shape}")
    print(f"Validation shape : {X_validation.shape}")
    print(f"Test shape       : {X_test.shape}")

    print("\nFeatures used by the model:")
    print(X_train.columns.tolist())

    # -- Select model --
    model_name = "random_forest"
    model_config_ = model_config["models"][model_name]

    # -- Train model --
    model = train_model(X_train, y_train, model_config_)

    # -- Find best threshold using validation data --
    # best_threshold = find_best_threshold(model,X_validation, y_validation,min_precision=0.50)

    threshold=0.5
    
    # -- Evaluate validation data --
    validation_metrics = evaluate_model(model, X_validation, y_validation, threshold=threshold, title="Validation Data Evaluation")

    print("\nValidation metrics:")
    for metric, value in validation_metrics.items():
        print(f"{metric}: {value}")
       
    # -- Save model --
    save_model(model, model_config["artefacts"][model_name])
    
    # -- Visualisation -- 
    visualize_all(df=validation_data, model=model, X=X_validation, y=y_validation, threshold=0.5,)

if __name__ == "__main__":
    run_pipeline()