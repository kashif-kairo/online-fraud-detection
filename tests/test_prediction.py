import pytest

from src.prediction import prepare_features, predict_fraud


@pytest.fixture
def sample_transaction():
    return {
        "step": 1,
        "type": "TRANSFER",
        "amount": 500000.0,
        "oldbalanceOrg": 500000.0,
        "newbalanceOrig": 0.0,
        "oldbalanceDest": 0.0,
        "newbalanceDest": 500000.0,
    }


def test_prepare_features(sample_transaction):
    features = prepare_features(sample_transaction)

    assert features.shape == (1, 14)
    assert features.columns.is_unique
    assert features.isnull().sum().sum() == 0


def test_predict_fraud_output(sample_transaction):
    result = predict_fraud(sample_transaction)

    assert result["is_fraud"] in [0, 1]
    assert 0 <= result["fraud_probability"] <= 1
    assert result["result"] in ["Fraudulent", "Legitimate"]


def test_invalid_transaction_type(sample_transaction):
    sample_transaction["type"] = "INVALID_TYPE"

    with pytest.raises(ValueError):
        prepare_features(sample_transaction)