from apiflask import Schema
from apiflask.fields import String, Integer
from apiflask.validators import Length, OneOf

from app.extensions import db
from app.models.registration import RegistrationModel

# define the student table
class StudentsModel(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    level = db.Column(db.String(8))
    courses = db.relationship('CoursesModel', secondary='student_courses_association', back_populates='students')

# define the schema for the student input
class StudentIn(Schema):
    name = String(required=True, validate=Length(0, 32))
    level = String(required=True, validate=OneOf(["HF", "AP", "PE", "ICT"]))

# define the schema for the output
class StudentOut(Schema):
    id = Integer()
    name = String()
    level = String()
