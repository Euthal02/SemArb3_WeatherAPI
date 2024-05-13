#!/usr/bin/python3
from apiflask import APIFlask, Schema
from flask_sqlalchemy import SQLAlchemy
from apiflask.fields import String, Integer
from apiflask.validators import OneOf, Length
from os import path as os_path

# define the schema for the post input
class PostStudentIn(Schema):
    name = String(required=True, validate=Length(0, 32))
    level = String(required=True, validate=OneOf(["HF", "AP", "PE", "ICT"]))

# define the schema for the output
class StudentOut(Schema):
    id = Integer()
    name = String()
    level = String()

# start the webserver
app = APIFlask(__name__)

# define DB value
basedir = os_path.abspath(os_path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os_path.join(basedir, 'app.db')

# create ORM (OBJECT RELATION MANAGEMENT)
db = SQLAlchemy(app)

# define the sudent table
class StudentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    level = db.Column(db.String(8))

# get all students
@app.get('/student')
@app.output(StudentOut(many=True))
def view_student():
    all_students = StudentModel.query.all()
    return StudentModel.query.all()

# get student by id
@app.get('/student/<int:id>')
@app.output(StudentOut)
def view_student_by_id(id):
    student = db.get_or_404(StudentModel, id)
    return student

# create new student
@app.post('/create_student')
@app.input(PostStudentIn, location='json')
@app.output(StudentOut, status_code=201)
def create_student(json_data):
    student = StudentModel(**json_data)
    db.session.add(student)
    db.session.commit()
    return student

# remove student by id
@app.delete('/remove_student/<int:id>')
@app.output(StudentOut)
def delete_student(id):
    student = db.get_or_404(StudentModel, id)
    db.session.delete(student)
    db.session.commit()
    return student

# create the database according to the model
with app.app_context():
    db.create_all()