
from flask import Flask,render_template, request


app = Flask(__name__)


@app.route('/')
def success():
    return render_template('index.html')

@app.route('/projects')
def project():
    return render_template('projects.html')

@app.route('/home', methods=["POST","GET"])
def landing():
    return render_template('home.html')

@app.route('/profile', methods=["POST","GET"])
def profile():
    return render_template('profile.html')

@app.route('/projects_search', methods=["POST","GET"])
def projects_search():
    return render_template('projects_search.html')    


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
