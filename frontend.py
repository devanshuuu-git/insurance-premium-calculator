import streamlit as st
import requests
from typing import Any, Dict

st.set_page_config(page_title="Insurance Premium Predictor", layout="centered")


def _post_json(url: str, payload: Dict[str, Any]) -> requests.Response:
    return requests.post(url, json=payload, timeout=30)


def _normalize_prediction_response(data: Dict[str, Any]) -> Dict[str, Any]:
    prediction = data.get("prediction")
    if isinstance(prediction, dict):
        return prediction

    nested = data.get("predicted_category")
    if isinstance(nested, dict):
        return nested

    if "predicted_category" in data:
        return {"predicted_category": data.get("predicted_category")}

    return data


with st.sidebar:
    st.header("Settings")
    api_base_url = st.text_input("API base URL", value="http://127.0.0.1:8000")
    predict_endpoint = api_base_url.rstrip("/") + "/predict"


st.title("Insurance Premium Predictor")
st.write("Enter details to get the predicted premium category.")


col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=1, max_value=120, value=30, step=1)
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.5)
    income_lpa = st.number_input("Income (LPA)", min_value=0.1, max_value=500.0, value=10.0, step=0.5)

with col2:
    height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.70, step=0.01, format="%.2f")
    city = st.text_input("City", value="Mumbai", max_chars=20)
    occupation = st.selectbox(
        "Occupation",
        options=[
            "retired",
            "freelancer",
            "student",
            "government_job",
            "business_owner",
            "unemployed",
            "private_job",
        ],
        index=6,
    )
    

smoker = st.checkbox("Smoker", value=False)


payload = {
    "age": int(age),
    "weight": float(weight),
    "height": float(height),
    "income_lpa": float(income_lpa),
    "smoker": bool(smoker),
    "city": city.strip(),
    "occupation": occupation,
}


disabled = payload["city"] == ""

if st.button("Predict", type="primary", disabled=disabled):
    try:
        response = _post_json(predict_endpoint, payload)
        if response.status_code != 200:
            st.error(f"API error: {response.status_code}\n\n{response.text}")
        else:
            data = response.json()
            prediction = _normalize_prediction_response(data)
            predicted_category = prediction.get("predicted_category")
            confidence = prediction.get("confidence")
            class_probabilities = prediction.get("class_probabilities")
            st.success("Prediction received")
            st.subheader("Predicted category")
            st.write(predicted_category)

            if confidence is not None:
                st.subheader("Confidence")
                st.write(confidence)

            if isinstance(class_probabilities, dict) and class_probabilities:
                st.subheader("Class probabilities")
                st.json(class_probabilities)
            with st.expander("Request payload"):
                st.json(payload)
            with st.expander("Full API response"):
                st.json(data)
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")