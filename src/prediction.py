import joblib
import pandas as pd
from pathlib import Path

# Paths to saved artifacts
MODEL_DIR = Path(__file__).resolve().parent.parent / "model"

model = joblib.load(MODEL_DIR / "random_forest.pkl")
preprocessor = joblib.load(MODEL_DIR / "preprocessor.pkl")


NUMERICAL_FEATURES = [
    "step",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "origin_balance_change",
    "origin_expected_balance",
    "destination_balance_change",
]

TYPE_COLUMNS = [
    "type_CASH_IN",
    "type_CASH_OUT",
    "type_DEBIT",
    "type_PAYMENT",
    "type_TRANSFER",
]


def prepare_features(transaction: dict) -> pd.DataFrame:
    """Create the exact features expected by the trained model."""

    transaction_type = transaction["type"]

    if transaction_type not in [
        "CASH_IN",
        "CASH_OUT",
        "DEBIT",
        "PAYMENT",
        "TRANSFER",
    ]:
        raise ValueError("Invalid transaction type.")

    # Create numerical and engineered features
    features = {
        "step": transaction["step"],
        "amount": transaction["amount"],
        "oldbalanceOrg": transaction["oldbalanceOrg"],
        "newbalanceOrig": transaction["newbalanceOrig"],
        "oldbalanceDest": transaction["oldbalanceDest"],
        "newbalanceDest": transaction["newbalanceDest"],
    }

    features["origin_balance_change"] = (
        features["oldbalanceOrg"] - features["newbalanceOrig"]
    )

    features["origin_expected_balance"] = (
        features["oldbalanceOrg"] - features["amount"]
    )

    features["destination_balance_change"] = (
        features["newbalanceDest"] - features["oldbalanceDest"]
    )

    # Scale numerical features using the saved preprocessor
    numerical_df = pd.DataFrame(
        [features],
        columns=NUMERICAL_FEATURES,
    )

    scaled_values = preprocessor.transform(numerical_df)

    scaled_df = pd.DataFrame(
        scaled_values,
        columns=NUMERICAL_FEATURES,
    )

    # One-hot encode transaction type
    type_features = {
        column: int(column == f"type_{transaction_type}")
        for column in TYPE_COLUMNS
    }

    type_df = pd.DataFrame([type_features])

    # Preserve the training feature order
    final_features = pd.concat(
        [scaled_df, type_df[TYPE_COLUMNS]],
        axis=1,
    )

    return final_features


def predict_fraud(transaction: dict) -> dict:
    """Predict whether a transaction is fraudulent."""

    features = prepare_features(transaction)

    prediction = int(model.predict(features)[0])
    fraud_probability = float(model.predict_proba(features)[0][1])

    return {
        "is_fraud": prediction,
        "fraud_probability": round(fraud_probability, 4),
        "result": "Fraudulent" if prediction == 1 else "Legitimate",
    }