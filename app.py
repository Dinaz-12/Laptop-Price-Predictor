from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

# -----------------------------
# Load model ONCE (best practice)
# -----------------------------
MODEL_PATH = os.path.join("model", "predictor.pickle")
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# -----------------------------
# Category lists MUST match training columns (30 features total)
# Total = 4 base + 9 + 6 + 4 + 4 + 3 = 30
# -----------------------------
company_list = ['acer', 'apple', 'asus', 'dell', 'hp', 'lenovo', 'msi', 'toshiba', 'other']
typename_list = ['2in1convertible', 'gaming', 'netbook', 'notebook', 'ultrabook', 'workstation']
opsys_list = ['linux', 'mac', 'other', 'windows']
cpu_list = ['amd', 'intelcorei3', 'intelcorei5', 'other']   # NOTE: no i7 (to match training)
gpu_list = ['amd', 'intel', 'nvidia']                       # NOTE: no "other" (to match training)


def one_hot_extend(feature_list, options, selected):
    """Append one-hot encoded vector for selected option."""
    for opt in options:
        feature_list.append(1 if opt == selected else 0)


@app.route("/", methods=["GET", "POST"])
def index():
    prediction_value = None
    error_msg = None

    if request.method == "POST":
        try:
            # ---- Read inputs ----
            ram = request.form.get("ram", "").strip()
            weight = request.form.get("weight", "").strip()

            company = request.form.get("company", "").strip()
            typename = request.form.get("typename", "").strip()
            opsys = request.form.get("opsys", "").strip()
            cpuname = request.form.get("cpuname", "").strip()
            gpuname = request.form.get("gpuname", "").strip()

            # Checkbox: if checked => "on", else None
            touchscreen = 1 if request.form.get("touchscreen") else 0
            ips = 1 if request.form.get("ips") else 0

            # ---- Basic validation ----
            if ram == "" or weight == "":
                raise ValueError("Please enter RAM and Weight.")

            # ---- Build feature vector (30 features) ----
            feature_list = []
            feature_list.append(int(ram))
            feature_list.append(float(weight))
            feature_list.append(touchscreen)
            feature_list.append(ips)

            one_hot_extend(feature_list, company_list, company)
            one_hot_extend(feature_list, typename_list, typename)
            one_hot_extend(feature_list, opsys_list, opsys)
            one_hot_extend(feature_list, cpu_list, cpuname)
            one_hot_extend(feature_list, gpu_list, gpuname)

            # Debug (optional)
            # print("Feature count:", len(feature_list))
            # print(feature_list)

            # ---- Predict ----
            pred = model.predict([feature_list])[0]
            prediction_value = round(float(pred), 2)

        except Exception as e:
            error_msg = str(e)

    return render_template("index.html", prediction=prediction_value, error=error_msg)


if __name__ == "__main__":
    app.run(debug=True)
