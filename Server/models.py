from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
import re


metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String, nullable = False)
    created_at = db.Column(db.DateTime(), server_default = db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate = db.func.now)

    orders = db.relationship("Order", backref = "users")
    reviews = db.relationship("Review", backref = "users")

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
    

class Commodity(db.Model, SerializerMixin):
    __tablename__ = 'commodities'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Integer)
    category = db.Column(db.String)
    imageUrl = db.Column(db.String)
    rating = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(), server_default = db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate = db.func.now)

    order = db.relationship("Order", backref = "commodities")
    reviews = db.relationship("Review", backref = "commodities")

    def __repr__(self):
        return f"Commodity name: {self.name}"
    
    @validates("rating")
    def validat_rating(self, key, rating):
        if rating <= 0 or rating > 6:
            raise ValueError ("Enter a rating between 0 and 6!")
        return rating
    

class Order(db.Model, SerializerMixin):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.String)
    orderDate = db.Column(db.DateTime(), server_default = db.func.now())
    price = db.Column(db.Integer)
    status = db.Column(db.String)
    updated_at = db.Column(db.DateTime(), onupdate = db.func.now())


    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    commodities_id = db.Column(db.Integer, db.ForeignKey("commodities.id"))


    payments = db.relationship("Payment", backref = "orders")
    

    def __repr__(self):
        return f"Order id: {self.order_id}"
    
class Payment(db.Model, SerializerMixin):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key = True)
    paymentDate = db.Column(db.DateTime(), server_default = db.func.now())
    paymentMethod = db.Column(db.String)
    amount = db.Column(db.Integer)

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))



    def __repr__(self):
        return f"Payment Amount: {self.amount}"
    

class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key = True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String)
    created_at = db.Column(db.DateTime(), server_default = db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate = db.func.now())

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


