import streamlit as st
from src.prediction import predict_fraud

# Page configuration
st.set_page_config(
    page_title="Online Fraud Detection",
    page_icon="🛡️",
    layout="centered"
)

# Application title
st.title("🛡️ Online Fraud Detection")
st.write("Enter the transaction details to check whether it is fraudulent.")

st.divider()

# Transaction input form
with st.form("transaction_form"):

    step = st.number_input(
        "Transaction Step",
        min_value=0,
        value=1,
        step=1
    )

    transaction_type = st.selectbox(
        "Transaction Type",
        ["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]
    )

    amount = st.number_input(
        "Transaction Amount",
        min_value=0.0,
        value=500000.0
    )

    col1, col2 = st.columns(2)

    with col1:
        oldbalanceOrg = st.number_input(
            "Sender's Previous Balance",
            min_value=0.0,
            value=500000.0
        )

        newbalanceOrig = st.number_input(
            "Sender's New Balance",
            min_value=0.0,
            value=0.0
        )

    with col2:
        oldbalanceDest = st.number_input(
            "Receiver's Previous Balance",
            min_value=0.0,
            value=0.0
        )

        newbalanceDest = st.number_input(
            "Receiver's New Balance",
            min_value=0.0,
            value=500000.0
        )

    submitted = st.form_submit_button(
        "Check Transaction",
        use_container_width=True
    )

# Prediction
if submitted:
    transaction = {
        "step": step,
        "type": transaction_type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }

    try:
        result = predict_fraud(transaction)

        st.divider()

        if result["is_fraud"] == 1:
            st.error("🚨 FRAUD")
        else:
            st.success("✅ NOT FRAUD")

    except Exception:
        st.error("Prediction failed. Please try again.")