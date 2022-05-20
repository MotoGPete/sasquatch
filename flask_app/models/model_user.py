
from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash
from flask_app.models import model_sightings
import re

DATABASE = 'exam'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pw_hash = data['pw_hash']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM users;"
    #     results = connectToMySQL(DATABASE).query_db(query)
    #     users = []
        
    #     for user in results:
    #         users.append( cls(user) )
    #     return users


    @classmethod
    def get_all_user_recipes(cls,data):
        query = "SELECT * FROM users LEFT JOIN sightings On sightings.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        user = cls( results[0] )
        for data in results:

            sighting_data = {
                'id' : data['recipes.id'],
                'location' : data['location'],
                'description' : data['description'],
                'date' : data['date'],
                'numsighted' : data['numsighted'],
                'created_at' : data['sightings.created_at'],
                'updated_at' : data['sightings.updated_at'],
                'user_id' : data['user_id']
            }
            user.recipes.append(model_sightings.Sighting( sighting_data ) )
        return user   
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , pw_hash , created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(pw_hash)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        
        if not results:
            return False
        return cls(results[0])   
    
    @staticmethod
    def validate_user(data:dict):
        is_valid = True

        if len(data['first_name']) < 3:
            is_valid = False
            flash("need a name bro")
        
        if len(data['last_name']) < 3:
            is_valid = False
            flash("need a last name bro")
        
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        
        if len (data['pw_hash']) < 3:
            flash("Invalid password")
            is_valid = False
        
        if data['pw_hash'] != data["pw_hash_confirm"]:
            flash("Passwords dont match!")
            is_valid = False       
        return is_valid

    @staticmethod
    def validate_login(data:dict):
        is_valid = True
        
        if not data['pw_hash']:
            flash("Invalid email/password")
            is_valid = False

        if not data['email']:
            flash("Invalid email/password")
            is_valid = False


        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email/password")
            is_valid = False


        return is_valid