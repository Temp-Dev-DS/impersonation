from flask import Flask, render_template
from glob import glob
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    # return render_template('hello.html', tite="flask test", name=name)

@app.route('/monomane')
def monomane():
    sound_list = glob('static/sound/*')
    sound_list = [i.split('/')[-1].replace('.mp3', '') for i in sound_list]
    print('sound_list:\n', sound_list)
    return render_template('monomane.html', sound_list=sound_list)


@app.route('/monomane_result')
def monomane_result():
    return render_template('result.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

