
from flask import Flask,render_template, request


app = Flask(__name__)


@app.route('/')
def success():
    return render_template('index.html')

@app.route('/projects')
def success():
    return render_template('projects.html')

if __name__ == '__main__':
    app.run()
