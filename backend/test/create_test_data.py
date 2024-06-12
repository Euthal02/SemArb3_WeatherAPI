from app.extensions import db
from app.models.users import UsersModel

# Hilfsfunktion (Testdaten erstellen, Tabellen erstellen)
def create_test_data():
    db.drop_all() # dieser Befehl löscht alle vorhandenen Datenbankeintraege und Tabellen
    db.create_all()

    # Beispieldaten
    users = [
        {'name': 'test', 'email': 'test@test.ch', 'password': 'test', 'is_admin': 1}
    ]
    for user_data in users:
        user = UsersModel(**user_data)
        db.session.add(user)

    db.session.commit()
