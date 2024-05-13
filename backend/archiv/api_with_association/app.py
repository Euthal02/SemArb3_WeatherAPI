#!/usr/bin/python3
from apiflask import APIFlask, Schema
from flask_sqlalchemy import SQLAlchemy
from apiflask.fields import String, Integer
from apiflask.validators import OneOf, Length, Range
from os import path as os_path
from os import environ as os_environ

# start the webserver
app = APIFlask(__name__)

# define DB value
basedir = os_path.abspath(os_path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os_environ.get('DATABASE_URI')\
        or 'sqlite:///' + os_path.join(basedir, 'app.db')

# create ORM (OBJECT RELATION MANAGEMENT)
db = SQLAlchemy(app)

####################################################
### Registration Model and Input / Output Schema ###
### ################################################

student_courses_association = db.Table(
    'student_courses_association',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
)

# define the schema for the student input
class RegistrationIn(Schema):
    student_id = Integer(required=True, validate=[Range(min=1, error="Value must be greater than 0")])
    course_id = Integer(required=True, validate=[Range(min=1, error="Value must be greater than 0")])

# define the schema for the output
class RegistrationOut(Schema):
    id = Integer()
    student_id = Integer()
    course_id = Integer()

class MessageOut(Schema):
    message = String()

###############################################
### Student Model and Input / Output Schema ###
### ###########################################

# define the student table
class StudentsModel(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    level = db.Column(db.String(8))
    courses = db.relationship('CoursesModel', secondary=student_courses_association, back_populates='students')

# define the schema for the student input
class StudentIn(Schema):
    name = String(required=True, validate=Length(0, 32))
    level = String(required=True, validate=OneOf(["HF", "AP", "PE", "ICT"]))

# define the schema for the output
class StudentOut(Schema):
    id = Integer()
    name = String()
    level = String()

##############################################
### Course Model and Input / Output Schema ###
##############################################

# define the courses table
class CoursesModel(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.String(32))
    topic = db.Column(db.String(32))
    students = db.relationship('StudentsModel', secondary=student_courses_association, back_populates='courses')

# define the schema for the student input
class CoursesIn(Schema):
    teacher = String(required=True, validate=Length(0, 32))
    topic = String(required=True, validate=Length(0, 32))

# define the schema for the output
class CoursesOut(Schema):
    id = Integer()
    teacher = String()
    topic = String()

########################################
## Standard Endpoints                 ##
########################################

# display information at the root
@app.get('/')
def root_path():
    return {'message': 'This is the root directory of my Flask Server. Try GET /student'}

########################################
## Student Endpoints                  ##
########################################

# get all students
@app.get('/student')
@app.output(StudentOut(many=True))
def view_student(database_table=StudentsModel):
    return database_table.query.all()

# get student by id
@app.get('/student/<int:id>')
@app.output(StudentOut)
def view_student_by_id(id, database_table=StudentsModel):
    student = db.get_or_404(database_table, id)
    return student

# create new student
@app.post('/create_student')
@app.input(StudentIn, location='json')
@app.output(StudentOut, status_code=201)
def create_student(json_data, database_table=StudentsModel):
    student = database_table(**json_data)
    db.session.add(student)
    db.session.commit()
    return student

# change the information for a db entry
@app.patch('/edit_student/<int:student_id>')
@app.input(StudentIn(partial=True), location='json')
@app.output(StudentOut)
def update_student(student_id, json_data, database_table=StudentsModel):
    student = db.get_or_404(database_table, student_id)
    for key, value in json_data.items():
        setattr(student, key, value)
    db.session.commit()
    return student

# remove student by id
@app.delete('/remove_student/<int:id>')
@app.output(StudentOut)
def delete_student(id, database_table=StudentsModel):
    student = db.get_or_404(database_table, id)
    db.session.delete(student)
    db.session.commit()
    return student

########################################
## Course Endpoints                   ##
########################################

# get all courses
@app.get('/course')
@app.output(CoursesOut(many=True))
def view_courses(database_table=CoursesModel):
    return database_table.query.all()

# get course by id
@app.get('/course/<int:id>')
@app.output(CoursesOut)
def view_courses_by_id(id, database_table=CoursesModel):
    course = db.get_or_404(database_table, id)
    return course

# create new course
@app.post('/create_course')
@app.input(CoursesIn, location='json')
@app.output(CoursesOut, status_code=201)
def create_course(json_data, database_table=CoursesModel):
    course = database_table(**json_data)
    db.session.add(course)
    db.session.commit()
    return course

# change the information for a db entry
@app.patch('/edit_course/<int:course_id>')
@app.input(CoursesIn(partial=True), location='json')
@app.output(CoursesOut)
def update_course(course_id, json_data, database_table=CoursesModel):
    course = db.get_or_404(database_table, course_id, )
    for key, value in json_data.items():
        setattr(course, key, value)
    db.session.commit()
    return course

# remove course by id
@app.delete('/remove_course/<int:id>')
@app.output(CoursesOut)
def delete_course(course_id, database_table=CoursesModel):
    course = db.get_or_404(database_table, course_id)
    db.session.delete(course)
    db.session.commit()
    return course

#################################
## combined endpoints         ###
#################################

def association_exists(student_id, course_id):
    query = db.exists().where(
        (student_courses_association.c.student_id == student_id) &
        (student_courses_association.c.course_id == course_id)
    )
    return db.session.query(query).scalar()

# register student for course
@app.post('/register_student_for_course')
@app.input(RegistrationIn, location='json')
@app.output(StudentOut, status_code=201)
def create_association(json_data):
    student_id = json_data["student_id"]
    course_id = json_data["course_id"]

    student = db.get_or_404(StudentsModel, student_id)
    course = db.get_or_404(CoursesModel, course_id)

    exists = association_exists(student_id, course_id)
    if exists:
        return {"message": "Association already exists"}
    else:
        student.courses.append(course)
        course.students.append(student)
        
        db.session.commit()
        return student

# remove student from course
@app.delete('/remove_student_from_course')
@app.input(RegistrationIn, location='json')
@app.output(StudentOut, status_code=201)
def delete_association(json_data):
    student_id = json_data["student_id"]
    course_id = json_data["course_id"]

    student = db.get_or_404(StudentsModel, student_id)
    course = db.get_or_404(CoursesModel, course_id)

    exists = association_exists(student_id, course_id)
    if exists:
        student.courses.remove(course)
        #course.students.remove(student)

        db.session.commit()
        return student
    else:
        return {"message": "Association already removed"}

# display courses for student by id

# display students for course by id


# create the database according to the model
with app.app_context():
    db.create_all()
