
from werkzeug.http import quote_etag
from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash
import re

# from flask_app.models.model_user import User
DATABASE = 'exam'

class Sighting:
    def __init__( self , data ):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.date = data['date']
        self.numsighted = data['numsighted']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings;"
        results = connectToMySQL(DATABASE).query_db(query)
        sightings = []
        for sighting in results:
            sightings.append( cls(sighting) )
        return sightings

    @classmethod
    def get_sighting(cls, data):
        query = "SELECT * FROM sightings WHERE id = %(id)s" 
        results = connectToMySQL(DATABASE).query_db(query,data)
        
        if not results:
            return False
        return cls(results[0])   
    
    # @classmethod
    # def get_all_email(cls):
    #     query = "SELECT email FROM users;"
    #     # make sure to call the connectToMySQL function with the schema you are targeting.
    #     results = connectToMySQL(DATABASE).query_db(query)
    #     # Create an empty list to append our instances of friends
    #     users = []
    #     # Iterate over the db results and create instances of friends with cls.
    #     for user in results:
    #         users.append( cls(user) )
    #     return users

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO sightings ( location , description , date , numsighted, created_at, updated_at , user_id ) VALUES ( %(location)s , %(description)s , %(date)s , %(numsighted)s,  NOW() , NOW() , %(user_id)s );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(DATABASE).query_db( query, data )
        
    @classmethod
    def update_sighting(cls, data):
        query = "UPDATE sightings SET location = %(location)s , description = %(description)s, date = %(date)s , numsighted = %(numsighted)s ,  user_id = %(user_id)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)



    @classmethod
    def delete_sighting(cls, data:dict):
        query = 'DELETE FROM sightings WHERE id = %(id)s;'
        return connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return False
        else:
            return cls(results[0])

    @staticmethod
    def validate_sighting(data:dict):
        is_valid = True

        if len(data['location']) < 3:
            is_valid = False
            flash("location required")
        if len(data['description']) < 3:
            is_valid = False
            flash("description required")
        if not (data['date']):
            is_valid = False
            flash("need a date")
        if not (data['numsighted']):
            flash('number sighted required, did you even see one bro?')   
        return is_valid

    # @staticmethod
    # def validate_login(data:dict):
    #     is_valid = True
    #     if not data['pw_hash']:
    #         flash("Not a User")
    #         is_valid = False
    #     if not EMAIL_REGEX.match(data['email']): 
    #         flash("Invalid email address!")
    #         is_valid = False


    #     return is_valid