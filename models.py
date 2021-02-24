from flask import Flask
# from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
# from app import app

app = Flask(__name__)
# api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# ma = Marshmallow(app)

class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    summary = db.Column(db.String(500))

    def __repr__(self):
        return '<TodoModel %s>' % self.task

db.create_all()