from apiflask import Schema
from apiflask.fields import Integer, Float
from apiflask.validators import Range

from app.extensions import db

class RegistrationStudentIn(Schema):
    student_id = Integer(required=True, validate=[Range(min=1, error="Value must be greater than 0")])

class RegistrationCourseIn(Schema):
    course_id = Integer(required=True, validate=[Range(min=1, error="Value must be greater than 0")])

class RegistrationOut(Schema):
    course_id = Integer()
    student_id = Integer()
    mark = Float()

# Hilfstabelle für many to many Relation
class RegistrationModel(db.Model):
    __tablename__ = 'student_courses_association'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    mark = db.Column(db.Float)
