from flask import Flask,render_template, request, flash, redirect, url_for, session, logging
import mongo
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

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

class LoginForm(Form):
    contact = StringField('Contact',[validators.InputRequired(message="Input is mandatory!!!!"),validators.Regexp(regex='^[0-9]{10}$',message="Contact number invalid")])
    division = StringField('Division',[validators.InputRequired(message="Input is mandatory!!!!"),validators.Length(min=3,max=5)])
    year = StringField('Year_of_joining',[validators.InputRequired(message="Input is mandatory!!!!"),validators.Length(4, 4),validators.Regexp(regex="^[0-9][0-9]{3}$")])

@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        print("Collected sucessfully")
    return render_template('login.html',form=form)


@app.route('/projects_search', methods=["POST","GET"])
def projects_search():
    return render_template('projects_search.html')    


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
