from flask import Flask,render_template, request
import mongo

app = Flask(__name__)

@app.route('/')
def success():
    return render_template('home.html')

@app.route('/projects')
def project():
    return render_template('projects.html')

@app.route('/home', methods=["POST","GET"])
def landing():
    return render_template('home.html')

@app.route('/profile', methods=["POST","GET"])
def profile():
    return render_template('profile.html')

@app.route('/faculty', methods=["POST","GET"])
def faculty():
    # result = mongo.facultyCollection.insert_one({
    #     "faculty_id":"2",
    #     "faculty_name":"Amit Singh",
    #     "faculty_email":"amit.singh@ves.ac.in"
    # })
    result = mongo.facultyCollection.find()
    for obj in result:
        print(obj)
    return render_template('faculty.html')
    return "New"

@app.route('/projects_search', methods=["POST","GET"])
def projects_search():
    return render_template('projects_search.html')    


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
