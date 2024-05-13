from apiflask import Schema
from apiflask.fields import String, Integer
from apiflask.validators import Length

from app.extensions import db
from app.models.registration import RegistrationModel

# define the courses table
class CoursesModel(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.String(32))
    topic = db.Column(db.String(32))
    students = db.relationship('StudentsModel', secondary='student_courses_association', back_populates='courses')

# define the schema for the student input
class CoursesIn(Schema):
    teacher = String(required=True, validate=Length(0, 32))
    topic = String(required=True, validate=Length(0, 32))

# define the schema for the output
class CoursesOut(Schema):
    id = Integer()
    teacher = String()
    topic = String()
