from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from models import TodoModel, db
# app = Flask(__name__)
# api = Api(app)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


# class TodoModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     task = db.Column(db.String(200))
#     summary = db.Column(db.String(500))

#     def __repr__(self):
#         return '<TodoModel %s>' % self.task

# db.create_all()

# todos = {
#     1:{'task': 'Connect web or mobile applications to databases and servers via REST APIs 111', 'summary':'databases and servers via REST APIs'
#     },
#     2:{'task': 'Connect web or mobile applications to databases and servers via REST APIs 222', 'summary':'databases and servers via REST APIs'
#     },
#     3:{'task': 'Connect web or mobile applications to databases and servers via REST APIs 333', 'summary':'databases and servers via REST APIs'
#     }
# }

task_post_args = reqparse.RequestParser()
task_post_args.add_argument('task', type=str, help='Task is required', required=True)
task_post_args.add_argument('summary', type=str, help='summary is required', required=True)

#for update
task_put_args = reqparse.RequestParser()
task_put_args.add_argument('task', type=str)
task_put_args.add_argument('summary', type=str)

resources_fields = {
    'id':fields.Integer,
    'task':fields.String,
    'summary':fields.String
}

# controllers class
class Todos(Resource):
    def get(self):
        tasks = TodoModel.query.all()
        todos = {}
        for task in tasks:
            todos[task.id] = {'task':task.task, 'summary':task.summary}
        return todos



class Todo(Resource):
    @marshal_with(resources_fields)
    def get(self, todo_id):
        task = TodoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort(404, 'Task with this ID already taken!')
        return task

    @marshal_with(resources_fields)
    def post(self, todo_id):
        args = task_post_args.parse_args()
        task = TodoModel.query.filter_by(id=todo_id).first()
        if task:
            abort(409, 'Task with this ID already taken!')

        todo = TodoModel(id=todo_id, task=args['task'], summary=args['summary'])
        db.session.add(todo)
        db.session.commit()
        return 201, todo

    @marshal_with(resources_fields)
    def put(self, todo_id):
        args = task_put_args.parse_args()
        task = TodoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort(404, 'Task is not found!')
        if args['task']:
            task.task  = args['task']
    
        if args['summary']:
            task.summary = args['summary']
        db.session.commit()
        return task  

    # @marshal_with(resources_fields)
    def delete(self, todo_id):
        task = TodoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort(404, 'Task is not found!')
        db.session.delete(task)
        
        return 204, 'todo deleted successful'