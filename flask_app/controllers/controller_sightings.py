from flask_app import app
from flask import render_template, request, redirect, session, flash, jsonify
from flask_app.models import model_sightings, model_user
import requests, os

@app.route('/get_episodes')
def get_episodes():
    # now we inject the query into our string
    r = requests.get("https://www.buzzsprout.com/147064/9558620.json")
    # we must keep in line with JSON format.
    # requests has a method to convert the data coming back into JSON.
    episode = jsonify( r.json() )
    return render_template("episodes.html", episode = episode)










@app.route('/sighting/new')
def new_sighting():
    user = model_user.User.get_by_email({'email': session['email']})
    if not user:
        return redirect('/')
    
    return render_template('sighting_new.html')
















@app.route('/sighting/create', methods=["POST"])
def sighting_create():
    user = model_user.User.get_by_email({'email': session['email']})
    if not user:
        return redirect('/')

    is_valid = model_sightings.Sighting.validate_sighting(request.form)
    
    if not is_valid:
        return redirect('/sighting/new')

    data = {
        'user_id' : session['user_id'],
        "location" : request.form['location'],
        "description" : request.form['description'],
        "date" : request.form["date"],
        "numsighted" : request.form['numsighted']
    } 

    model_sightings.Sighting.save(data)
        
    return redirect('/sighting/new')







@app.route("/sighting/update/<int:id>", methods=["POST"] )
def update_the_sighting(id):
    user = model_user.User.get_by_email({'email': session['email']})
    if not user:
        return redirect('/')
    sighting = model_sightings.Sighting.get_sighting({"id": id})
    if user.id != sighting.user_id:
        return render_template("sighting_edit.html", sighting = sighting )

    data = {
        **request.form,
        "id": id,
        "user_id": user.id
    }
    
    is_valid = model_sightings.Sighting.validate_sighting(request.form)
    

    if not is_valid:
        
        return render_template("sighting_edit.html", sighting = sighting )
    
    model_sightings.Sighting.update_sighting(data)
    return redirect('/dashboard')







@app.route("/sighting/edit/<int:id>")
def edit_sighting(id):
    user = model_user.User.get_by_email({'email': session['email']})
    if not user:
        return redirect('/')

    sighting = model_sightings.Sighting.get_sighting({"id": id})


    return render_template("sighting_edit.html", sighting= sighting)






@app.route('/sighting/delete/<int:id>')
def sighting_delete(id):
    user = model_user.User.get_by_email({'email': session['email']})
    if not user:
        return redirect('/')

    model_sightings.Sighting.delete_sighting({"id": id})
    return redirect('/dashboard')

# @app.route('/sightings/<int:id>')
# def view_sighting(id):
#     user = model_user.User.get_by_email({'email': session['email']})
#     if not user:
#         return redirect('/')

#     sighting = model_sightings.Sighting.get_sighting(id)
#     # patriots = model_user.User.get_all_users()
#     return render_template("sighting_show.html", sighting = sighting, )