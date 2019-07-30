from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    context = {
        'message': 'I am a cow now.'
    }
    return render_template('index.html', **context)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
