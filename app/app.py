from flask import Flask, render_template, jsonify, request
import datetime
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

@app.route('/monomane', methods=['POST'])
def uploaded_wav():
    fname = "../static/data/" + datetime.now().strftime('%m%d%H%M%S') + ".wav"
    with open(f"{fname}", "wb") as f:
        f.write(request.files['data'].read())
    print(f"posted sound file: {fname}")
    return jsonify({"data": fname})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

