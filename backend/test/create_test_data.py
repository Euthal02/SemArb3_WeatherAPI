from app.extensions import db
from app.models.student import StudentsModel
from app.models.course import CoursesModel
from app.models.users import UsersModel

# Hilfsfunktion (Testdaten erstellen, Tabellen erstellen)
def create_test_data():
    db.drop_all() # dieser Befehl löscht alle vorhandenen Datenbankeintraege und Tabellen
    db.create_all()

    # Beispieldaten
    students = [
        {'name': 'Freda Kids', 'level': 'HF'},
        {'name': 'Sam Sung', 'level': 'HF'},
        {'name': 'Chris P. Bacon', 'level': 'AP'},
        {'name': 'Saad Maan', 'level': 'PE'}
    ]
    for student_data in students:
        student = StudentsModel(**student_data)
        db.session.add(student)

    # create an additional student and safe ref for later
    student_ref = StudentsModel(name='Mega Tron', level='HF')
    db.session.add(student_ref)

    courses = [
        {'topic': 'M231 Security'},
        {'topic': 'M254 BPMN'}
    ]
    for course_data in courses:
        course = CoursesModel(**course_data)
        db.session.add(course)

    # create an additional course and safe ref for later
    course_ref = CoursesModel(topic='M347 Kubernetes')
    db.session.add(course_ref)
    student_ref.courses.append(course_ref)

    # Beispieldaten
    users = [
        {'name': 'test', 'email': 'test@test.ch', 'password': 'test'}
    ]
    for user_data in users:
        user = UsersModel(**user_data)
        db.session.add(user)

    # create an additional student and safe ref for later
    student_ref = StudentsModel(name='Mega Tron', level='HF')
    db.session.add(student_ref)

    db.session.commit()
