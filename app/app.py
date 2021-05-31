from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    # return render_template('hello.html', tite="flask test", name=name)

@app.route('/monomane')
def monomane():
    return render_template('monomane.html')


@app.route('/monomane_result')
def monomane_result():
    return render_template('result.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

