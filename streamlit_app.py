import streamlit as st
import pickle
import numpy as np

# Load model
@st.cache_resource
def load_model():
    with open("model/predictor.pickle", "rb") as f:
        return pickle.load(f)

model = load_model()

st.set_page_config(page_title="Laptop Price Predictor", layout="centered")

st.title("💻 Laptop Price Predictor")

# Inputs
ram = st.number_input("RAM (GB)", min_value=2, max_value=64, step=2)
weight = st.number_input("Weight (kg)", min_value=0.5, max_value=5.0, step=0.1)

touchscreen = st.checkbox("Touchscreen")
ips = st.checkbox("IPS Display")

company = st.selectbox(
    "Company",
    ["acer", "apple", "asus", "dell", "hp", "lenovo", "msi", "toshiba", "other"]
)

typename = st.selectbox(
    "Type",
    ["2in1convertible", "gaming", "netbook", "notebook", "ultrabook", "workstation"]
)

opsys = st.selectbox(
    "Operating System",
    ["linux", "mac", "other", "windows"]
)

cpu = st.selectbox(
    "Processor",
    ["amd", "intelcorei3", "intelcorei5", "intelcorei7", "other"]
)

gpu = st.selectbox(
    "GPU",
    ["amd", "intel", "nvidia", "other"]
)

# Feature builder
def build_features():
    features = []
    features.append(int(ram))
    features.append(float(weight))
    features.append(1 if touchscreen else 0)
    features.append(1 if ips else 0)

    def one_hot(lst, val):
        return [1 if item == val else 0 for item in lst]

    features += one_hot(
        ["acer", "apple", "asus", "dell", "hp", "lenovo", "msi", "toshiba", "other"],
        company
    )

    features += one_hot(
        ["2in1convertible", "gaming", "netbook", "notebook", "ultrabook", "workstation"],
        typename
    )

    features += one_hot(
        ["linux", "mac", "other", "windows"],
        opsys
    )

    features += one_hot(
        ["amd", "intelcorei3", "intelcorei5", "intelcorei7", "other"],
        cpu
    )

    features += one_hot(
        ["amd", "intel", "nvidia", "other"],
        gpu
    )

    return np.array(features).reshape(1, -1)

# Predict
if st.button("🔮 Predict Price"):
    X = build_features()

    if X.shape[1] != model.n_features_in_:
        st.error(
            f"Feature mismatch! Model expects {model.n_features_in_} features, "
            f"but got {X.shape[1]}"
        )
    else:
        price = model.predict(X)[0]
        st.success(f"💰 Estimated Laptop Price: €{round(price, 2)}")
