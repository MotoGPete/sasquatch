from flask import Flask, render_template, request, redirect

from flask_app.controllers import controller_user, controller_sightings
from flask_app import app

if __name__ == "__main__":      
    app.run(debug=True)