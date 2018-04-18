from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
import mongo
from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, validators
from wtforms_components import read_only
from passlib.hash import sha256_crypt 
from functools import wraps
from bson.objectid import ObjectId

app = Flask(__name__)

@app.route('/')
def success():
    projects = list(mongo.projectCollection.find())
    numResults = min(len(projects),4)
    return render_template('home.html',projects=projects, numResults=numResults)

@app.route('/home', methods=["POST","GET"])
def landing():
    projects = list(mongo.projectCollection.find())
    numResults = min(len(projects),4)
    return render_template('home.html',projects=projects, numResults=numResults)



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
    year = SelectField("Year of joining", choices=[(year, year) for year in range(2010, 2018)])

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
            result = mongo.studentCollection.find_one({
                    "email": email
                },
                {
                    "password": 1,
                    "name": 1,
                    "email": 1,
                    "_id": 1
                }
            )
            if sha256_crypt.verify(password_to_verify, result['password']):
                session['logged_in'] = True
                session['email'] = result['email']
                session['username'] = result['name']
                session['id'] = str(result['_id'])
                flash('Logged In Successfully', 'success')
                return redirect(url_for('home'))
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

@app.route('/logout', methods=["POST","GET"])
@is_logged_in
def logout():
    session['logged_in'] = False
    flash('You are logged out successfully','success')
    return redirect(url_for('login'))


@app.route('/search-results', methods=['POST','GET'])
def projects_search():
    projects = list(mongo.projectCollection.find())
    numResults = min(len(projects),4)
    return render_template('projects_search.html',projects=projects, numResults=numResults)

class UploadProject(Form):
    proj_leader = StringField('Project Leader registered email ID', [validators.InputRequired(message="Input Mandatory"), validators.Regexp(regex='^[0-9]{4}[a-z]+.[a-z]+@ves.ac.in$',message="Inappropriate Email ID")])
    proj_member = StringField('Enter registered email ID of other members(should not exceed more than 3 member)',[validators.InputRequired(message="Input Mandatory")], render_kw={"placeholder": "Enter names as comma separated values: eg: xd, xd, xd,..."})
    proj_name = StringField('Project Name', [validators.InputRequired(message="Input is mandatory!!!!"), validators.Length(min=2, max=40)])
    project_description = TextAreaField('Project Description', [validators.InputRequired(message="Input is mandatory!!!!") ,validators.Length(min=20, max=180)])
    category = SelectField(
        'Category',
        choices=[('Data Mining', 'Data Mining'), ('AI', 'Artificial Intelligence'), ('Security', 'Security'),
            ('Networking', 'Networking'), ('IOT', 'IOT'), ('Application Development', 'Application Development'),
            ('Graphics/Virtual Reality', 'Graphics/Virtual Reality'), ("NLP", "Natural Language Processing")
        ]
    )
    status = SelectField("Status", choices=[('PC', "Partially Completed"), ('C', 'Completed')])
    semester = SelectField("Semester", choices=[('3', 'Sem 3'), ('4', 'Sem 4'), ('5', 'Sem 5'), ('6', 'Sem 6'), ('7', 'Sem 7')])
    subject = StringField('Subject Name',[validators.InputRequired(message="Input is mandatory!!!!"), validators.Length(min=2, max=15)], render_kw={"placeholder": "If not part of academics enter non-academic"})
    academicYear = SelectField("Academic Year", choices=[(str(year), str(year)) for year in range(2010, 2018)])
    github = StringField('Github Repo',[validators.Regexp(regex='^https://github.com/[a-zA-Z0-9]+/$', message="pattern mismatch!!!")])
    endurance = TextAreaField('Your Experience', [validators.InputRequired(message="Input is mandatory!!!!") ,validators.Length(min=5, max=180)])

@app.route('/upload_projects', methods=["POST", "GET"])
@is_logged_in
def uploadProject():
    form = UploadProject(request.form)
    if request.method == 'POST' and form.validate():
        proj_leader = form.proj_leader.data
        proj_member = form.proj_member.data
        proj_name = form.proj_name.data
        description = form.project_description.data
        category = form.category.data
        status = form.status.data
        semester = form.semester.data
        subject = form.subject.data
        academicYear = form.academicYear.data
        github = form.github.data
        endurance = form.endurance.data
        member = list(proj_member.split(', '))
        if len(member) <= 3:
            try:
                memberID = []
                leader = mongo.studentCollection.find_one({
                    "email": proj_leader
                },{
                    "name": 1
                })
                for m in member:
                    result = mongo.studentCollection.find_one(
                        {"email": m},
                        {"name": 1}
                    )
                    memberID.append(str(result["_id"]))
                result = mongo.projectCollection.insert_one(
                    {
                        "project_name": proj_name,
                        "project_description": description,
                        "project_leader": leader["_id"],
                        "project_members": memberID,
                        "project_category": category,
                        "project_status": status,
                        "project_subject": subject,
                        "project_academic_year": academicYear,
                        "project_semester": semester,
                        "project_github_repo": github,
                        "project_experiences": endurance,
                        "project_rating": []

                    }
                )
                flash("Project uploaded sucessfully", "success")    
            except:    
                flash('Insertion Error Invalid member!!!!', "danger")
        else:
            flash("Upload failed #(Members) can't exceed 4", "warning")
    return render_template('upload.html', form=form)

@app.route('/my-projects')
@is_logged_in
def my_project():
    projects = list(mongo.projectCollection.find( { '$or': [ { "project_leader": session['id'] }, { "project_members": session['id'] } ] }))
    numResults = min(len(projects),4)
    return render_template('projects_search.html',projects=projects, numResults=numResults)

@app.route('/project', methods=["GET"])
def project():
    project_id = request.args['id']
    project = mongo.projectCollection.find_one(ObjectId(project_id))
    print(project['project_rating'][0]['comments'])
    return render_template('projects.html',project = project)

if __name__ == '__main__':
    app.secret_key = "secret123"
    app.run(host='127.0.0.1', port=8000, debug=True)
