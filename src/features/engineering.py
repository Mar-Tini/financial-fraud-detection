import pandas as pd # type: ingore 
from pathlib import Path
import joblib # type: ignore 



def recalculate_balances(data: pd.DataFrame) -> pd.DataFrame:
    # -- Copy dataset --
    data = data.copy()

    # -- Identify transaction types safely --
    cash_out = data.get("type_CASH_OUT", pd.Series(0, index=data.index)).eq(1)
    transfer = data.get("type_TRANSFER", pd.Series(0, index=data.index)).eq(1)
    cash_in = data.get("type_CASH_IN", pd.Series(0, index=data.index)).eq(1)

    outgoing_mask = cash_out | transfer
    incoming_mask = cash_in | transfer | cash_out

    # -- Recalculate origin balance --
    data.loc[outgoing_mask, "newbalanceOrig"] = (
        data.loc[outgoing_mask, "oldbalanceOrg"]
        - data.loc[outgoing_mask, "amount"]
    ).clip(lower=0)

    # -- Recalculate destination balance --
    data.loc[incoming_mask, "newbalanceDest"] = (
        data.loc[incoming_mask, "oldbalanceDest"]
        + data.loc[incoming_mask, "amount"]
    )

    # -- Calculate balance changes --
    data["balance_change_orig"] = (
        data["newbalanceOrig"] - data["oldbalanceOrg"]
    )

    data["balance_change_dest"] = (
        data["newbalanceDest"] - data["oldbalanceDest"]
    )

    # -- Calculate consistency errors --
    data["balance_error_orig"] = (
        data["oldbalanceOrg"]
        - data["newbalanceOrig"]
        - data["amount"]
    ).where(outgoing_mask, 0)

    data["balance_error_dest"] = (
        data["newbalanceDest"]
        - data["oldbalanceDest"]
        - data["amount"]
    ).where(incoming_mask, 0)

    return data


def create_variables(train_data: pd.DataFrame, validation_data: pd.DataFrame, test_data: pd.DataFrame):
    # -- Copy datasets --
    datasets = [
        train_data.copy(),
        validation_data.copy(),
        test_data.copy(),
    ]

    for data in datasets:
        
        # -- Identify outgoing transactions --
        mask = data["type_CASH_OUT"].eq(1) | data["type_TRANSFER"].eq(1)

        # -- Recalculate original account balance --
        data.loc[mask, "newbalanceOrig"] = (
            data.loc[mask, "oldbalanceOrg"]
            - data.loc[mask, "amount"]
        ).clip(lower=0)

        # -- Create features --
        data["balance_change_orig"] = data["newbalanceOrig"] - data["oldbalanceOrg"]
        
        data["balance_error_orig"] = data["oldbalanceOrg"] - data["newbalanceOrig"] - data["amount"]
        
        # -- Remove identifiers --
        data.drop(
            columns=["nameOrig", "nameDest"],
            errors="ignore",
            inplace=True,
        )

    return datasets[0], datasets[1], datasets[2]

def split_features_target(train_data: pd.DataFrame, validation_data: pd.DataFrame, test_data: pd.DataFrame):
    
    # -- Recalculate balances --
    train_data = recalculate_balances(train_data)
    validation_data = recalculate_balances(validation_data)
    test_data = recalculate_balances(test_data)
    
    # -- Train --

    X_train = train_data.drop(columns=["isFraud"])
    y_train = train_data["isFraud"]

    # -- Validation --

    X_validation = validation_data.drop(columns=["isFraud"])
    y_validation = validation_data["isFraud"]

    # -- Test --

    X_test = test_data.drop(columns=["isFraud"])
    y_test = test_data["isFraud"]

    return (
        X_train,
        y_train,
        X_validation,
        y_validation,
        X_test,
        y_test
    )


def save_feature_engineer(feature_engineer, output_path: str):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(feature_engineer, path, compress=3)

    print(f"# -- Feature Engineering saved to: {path} --")


def feature_data(train_data: pd.DataFrame, validation_data: pd.DataFrame, test_data: pd.DataFrame):
    
    # -- Create features --
    train_data, validation_data, test_data = create_variables(
        train_data,
        validation_data,
        test_data
    )
    
    # -- Split features and target --
    return split_features_target(
        train_data,
        validation_data,
        test_data
    )