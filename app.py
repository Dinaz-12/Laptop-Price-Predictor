from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ram = request.form.get('ram')
        weight = request.form.get('weight')
        company = request.form.get('company')
        touchscreen = request.form.get('touchscreen')
        ips = request.form.get('ips')
        typename = request.form.get('typename')
        opsys = request.form.get('opsys')
        cpuname = request.form.get('cpuname')
        gpuname = request.form.get('gpuname')

        # -----------------------
        # Base numeric features
        # -----------------------
        feature_list = []
        feature_list.append(int(ram))
        feature_list.append(float(weight))
        feature_list.append(1 if touchscreen else 0)
        feature_list.append(1 if ips else 0)

        # -----------------------
        # Category lists
        # -----------------------
        company_list = ['acer', 'apple', 'asus', 'dell', 'hp', 'lenovo',
                        'msi', 'toshiba', 'other']
        typename_list = ['2in1convertible', 'gaming', 'netbook',
                         'notebook', 'ultrabook', 'workstation']
        opsys_list = ['linux', 'mac', 'other', 'windows']
        cpu_list = ['amd', 'intelcorei3', 'intelcorei5', 'intelcorei7', 'other']
        gpu_list = ['amd', 'intel', 'nvidia', 'other']

        # -----------------------
        # One-hot encoding helper
        # -----------------------
        def traverse(lst, value):
            for item in lst:
                feature_list.append(1 if item == value else 0)

        traverse(company_list, company)
        traverse(typename_list, typename)
        traverse(opsys_list, opsys)
        traverse(cpu_list, cpuname)
        traverse(gpu_list, gpuname)

        print("Feature vector:", feature_list)
        print("Total features:", len(feature_list))

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
