from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ram = request.form.get('ram')
        weight = request.form.get('weight')
        print(ram)
        print(weight)

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
