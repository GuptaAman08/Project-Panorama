from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
import mongo
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt 
from functools import wraps

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
    email = StringField('Email',[validators.InputRequired(message="Input is mandatory!!!!"),validators.Regexp(regex='^[0-9]{4}[a-z]+.[a-z]+@ves.ac.in$',message="Inappropriate Email ID")])
    name = StringField('Name',[validators.InputRequired(message="Input is mandatory!!!!"),validators.Regexp(regex="[a-zA-Z]+")])
    password = PasswordField('Password',[validators.DataRequired(message="Input is mandatory!!!!"), validators.EqualTo('confirm', message="Passwords do not match")])
    confirm = PasswordField('Confirm Password',[validators.InputRequired(message="Input is mandatory!!!!")])
    contact = StringField('Contact',[validators.InputRequired(message="Input is mandatory!!!!"),validators.Regexp(regex='^[0-9]{10}$',message="Contact number invalid")])
    division = StringField('Division',[validators.InputRequired(message="Input is mandatory!!!!"),validators.Length(min=3,max=5)])
    year = StringField('Year_of_joining',[validators.InputRequired(message="Input is mandatory!!!!"),validators.Length(4, 4),validators.Regexp(regex="^[0-9][0-9]{3}$")])

@app.route('/register',methods=['POST','GET'])
def register():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        name = form.name.data
        password = sha256_crypt.encrypt(str(form.password.data))
        contact = form.contact.data
        div = form.division.data
        year = form.year.data
        
        try:
            result = mongo.studentCollection.insert_one({
                "email": email,
                "name": name,
                "password": password,
                "contact": contact,
                "class": div,
                "year": year
            })
            flash('Registered successfully!!', 'success')
            return redirect(url_for('login'))
        except:
            flash('insertion error!!', 'danger')
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)

@app.route('/login', methods=["POST","GET"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_to_verify = request.form['password']
        
        try:
            print(email)
            result = mongo.studentCollection.find_one({
                    "email": email
                },
                {
                    "password": 1,
                    "name": 1,
                    "_id": 0
                }
            )
            if sha256_crypt.verify(password_to_verify, result['password']):
                session['logged_in'] = True
                session['username'] = result['name']
                flash('Logged In Successfully', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Incorrect username or password', 'danger')
                return render_template('login.html')
        except:
            flash('Couldnt find in DataBase', 'danger')
            return render_template('login.html')
    return render_template('login.html')    

#Checked if user is logged in 
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['logged_in']:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, Please login", "warning")
            return redirect(url_for('login'))
    return wrap

@app.route('/dashboard', methods=["POST","GET"])
@is_logged_in
def dashboard():
    return render_template('home.html')

@app.route('/logout', methods=["POST","GET"])
def logout():
    session['logged_in'] = False
    flash('You are logged out successfully','success')
    return redirect(url_for('login'))


@app.route('/projects_search', methods=["POST","GET"])
def projects_search():
    return render_template('projects_search.html')    


if __name__ == '__main__':
    app.secret_key = "secret123"
    app.run(host='127.0.0.1', port=8000, debug=True)
