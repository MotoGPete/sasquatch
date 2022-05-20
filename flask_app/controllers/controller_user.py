from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import model_user
from flask_app.models import model_sightings
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)

# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/logout')
def logout():
    del session['user_id']
    return redirect('/')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/login', methods=['POST'])
def login():
    
    is_valid = model_user.User.validate_login(request.form)
    if not is_valid:
        return redirect('/')
    
    user = model_user.User.get_by_email({'email': request.form['email']})
    if not user:
        flash("not a user email")
        return redirect('/')

    if not bcrypt.check_password_hash(user.pw_hash, request.form['pw_hash']):
        return redirect('/',)

    session['user_id'] = user.id,
    session['email'] = user.email
    
    
    
    return redirect("/dashboard")



@app.route('/sighting/<int:id>')
def view_sighting(id):
    user = model_user.User.get_by_email({'email': session['email']})
    if not user:
        return redirect('/')
    patriots = model_user.User.get_all_users()
    sighting = model_sightings.Sighting.get_sighting({"id": id})
    print(patriots)
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    return render_template("sighting_show.html", sighting = sighting, patriots = patriots, user= user )

@app.route('/dashboard')
def dash():
    sightings = model_sightings.Sighting.get_all()
    patriots = model_user.User.get_all_users()
    user = model_user.User.get_by_email({'email': session['email']})
    if session['user_id']: 
        return render_template('dashboard.html', user = user, sightings=sightings, patriots = patriots )
    else:
        return render_template('index.html')


@app.route('/user/create', methods=["POST"])
def create_user():
    is_valid = model_user.User.validate_user(request.form)
    
    if not is_valid:
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['pw_hash'])

    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'pw_hash' : pw_hash
    }
    model_user.User.save(data)
    return redirect('/')

@app.route('/user/<int:id>')
def show_user():
    pass