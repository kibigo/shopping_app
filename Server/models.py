from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
import re


metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class User:
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String, nullable = False)
    created_at = db.Column(db.DateTime(), server_default = db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate = db.func.now)

    def __repr__(self):
        return f'Customer: {self.firstname}'
    
    @validates("firstname", "lastname")
    def validate_names(self, key, value):
        if not value or not value.strip():
            raise ValueError(f"{key.capitalize()} cannot be empty")
        return value
    
    @validates("email")
    def validate_email(self, key, email):
        pattern = "^[a-z A-Z 0-9 .]+@[a-z A-Z]+\.[a-z A-Z]{2,3}$"

        if not re.search(pattern, email):
            raise ValueError(F"{email} is not a valid email")
        return email