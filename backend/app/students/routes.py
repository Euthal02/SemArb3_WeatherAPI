from app.students import bp 
from app.extensions import db
from app.auth import token_auth
from app.models.student import StudentsModel, StudentIn, StudentOut
from app.models.registration import RegistrationCourseIn, RegistrationModel
from app.models.course import CoursesOut, CoursesModel

def association_exists(table_a_id, table_b_id):
    association = RegistrationModel.query.filter_by(student_id=table_a_id, course_id=table_b_id).first()
    return association is not None

# get all students
@bp.get('/')
@bp.auth_required(token_auth)
@bp.output(StudentOut(many=True))
def view_student(database_table=StudentsModel):
    return database_table.query.all()

# get student by id
@bp.get('/<int:student_id>')
@bp.auth_required(token_auth)
@bp.output(StudentOut)
def view_student_by_id(student_id, database_table=StudentsModel):
    student = db.get_or_404(database_table, student_id)
    return student

# create new student
@bp.post('/create')
@bp.auth_required(token_auth)
@bp.input(StudentIn, location='json')
@bp.output(StudentOut, status_code=201)
def create_student(json_data, database_table=StudentsModel):
    student = database_table(**json_data)
    db.session.add(student)
    db.session.commit()
    return student

# change the information for a db entry
@bp.patch('/<int:student_id>/edit')
@bp.auth_required(token_auth)
@bp.input(StudentIn(partial=True), location='json')
@bp.output(StudentOut)
def update_student(student_id, json_data, database_table=StudentsModel):
    student = db.get_or_404(database_table, student_id)
    for key, value in json_data.items():
        setattr(student, key, value)
    db.session.commit()
    return student

# remove student by id
@bp.delete('/<int:student_id>/remove')
@bp.auth_required(token_auth)
@bp.output(StudentOut)
def delete_student(student_id, database_table=StudentsModel):
    student = db.get_or_404(database_table, student_id)
    db.session.delete(student)
    db.session.commit()
    return student

# register a student with a course
@bp.post('/<int:student_id>/register')
@bp.auth_required(token_auth)
@bp.input(RegistrationCourseIn, location='json')
@bp.output(StudentOut, status_code=201)
def register_course(student_id, json_data):
    course_id = json_data["course_id"]

    student = db.get_or_404(StudentsModel, student_id)
    course = db.get_or_404(CoursesModel, course_id)

    exists = association_exists(student_id, course_id)
    if exists:
        return student
    else:
        student.courses.append(course)
        course.students.append(student)
        db.session.commit()
        return student

# get all courses of a student
@bp.get('/<int:student_id>/courses')
@bp.auth_required(token_auth)
@bp.output(CoursesOut(many=True))
def get_student_courses(student_id, database_table=StudentsModel):
    student = db.get_or_404(database_table, student_id)
    courses = student.courses
    return courses

# remove student from course
@bp.delete('/<int:student_id>/unregister')
@bp.auth_required(token_auth)
@bp.input(RegistrationCourseIn, location='json')
@bp.output(StudentOut, status_code=201)
def delete_association(student_id, json_data):
    course_id = json_data["course_id"]

    student = db.get_or_404(StudentsModel, student_id)
    course = db.get_or_404(CoursesModel, course_id)

    exists = association_exists(student_id, course_id)
    if exists:
        student.courses.remove(course)
        course.students.remove(student)
        db.session.commit()
        return student
    else:
        return student
