---
layout: default
title: 3.1.4 Authentifizierung
parent: 3.1 Backend
grand_parent: 3. Hauptteil
nav_order: 314
---

# 3.1.4 Authentifizierung

Das Backend nutzt eine User Authentifzierung. Das bedeutet, man muss einen User mit Passwort besitzen, um das Backend zu nutzen.

Wir haben keine klassisches Registrierungsmethode, sondern wir haben uns darauf geeinigt, dass nur der Admin einen User erstellen kann.

Unsere Überlegung dabei ist, dass wenn sich ein Hacker selbst registrieren kann und direkt einen User erhält, dann macht das ganze User Management keinen Sinn.

Sollte aber die Userverwaltung in der Hand des Admins sein, kann man besser kontrollieren wer Zugriff auf die Applikation hat.

Für eine nächste Semesterarbeit, würde ich die Option mit dem Einladungslink umsetzen. Dies war jedoch im diesjährigen 50-Stunden Umfang nicht mehr drin.

Momentan haben wir also folgende Routen:

![User Routen](../ressources/images/backend/user_routen.PNG){: width="1000px" }

[Quelle Bild - Selbsterstellt](../anhang/600-quellen.html#61-bilder)

## CRUD Prinzip

### READ

Die beiden GET-Routen sind dazu da, User abzufragen, entweder limitiert auf eine User ID oder aber jegliche User. Diese beiden Routen stellen den READ Aspekt von CRUD dar. Die User ID eines Users wird automatisch generiert und spiegelt auch die Row ID in der Datenbanbk wieder.

### CREATE

#### User Registrierung

Mit den beiden POST-Routen kreiert man einen User und kann sich mit diesem Anmelden. Bei der Anmeldung wird ein JWT-Token generiert. Diese beiden Routen sind also CREATE nach dem CRUD Prinzip.

Um einen User zu erstellen werden folgende Attribute benötigt. Wie man hier sehen kann, kann man definieren ob ein User Admin Rechte hat. Admin Rechte bedeuten, dass man andere User erstellen kann. Ein User ohne Admin Rechte kann dies nicht.

``` json
{
  "email": "string",
  "is_admin": false,
  "name": "string",
  "password": "string"
}
```

Dies wird mit diesem Python-Directive bei der CREATE Route erzielt:

``` python
@token_auth.login_required(role="Admin")
...
def create_user(json_data, database_table=UsersModel):
    ...
```

Die Funktionszuweisung geschieht anschliessend im Auth.py.

Dort wird überprüft, welche Rolle der momentane User hat.

``` python
@token_auth.get_user_roles
def get_user_roles( user_auth_object ):
    current_user = UsersModel.verify_auth_token(user_auth_object.token)
    return UsersModel.get_roles(user=current_user)
```

Dieses Python Directive benötigt eine weitere Funktion im Users Modell:

``` python
class UsersModel(db.Model):
    __tablename__ = 'users'
    ...
    is_admin = db.Column(db.Boolean)
    ...

    def __init__( self, email, name, password, is_admin=False ):
        ...
        self.is_admin = is_admin
        ...
    
    @staticmethod
    def get_roles( user ):
        user_role = ["User"]
        if user.is_admin:
            user_role = ["Admin"]
        return user_role
```

#### Login

Beim Login werden anschliessend nur die EMail Addresse und das Passwort benötigt:

``` python
class LoginIn(Schema):
    email = String(required=True, validate=[Length(0, 128), Email()])
    password = String(required=True, validate=Length(0, 256))
```

Falls diese korrekt sind, wird der User einen JWT Token erhalten.
Dieser Token muss anschliessend bei jedem Requests mitgesendet werden.

``` python
class UsersModel(db.Model):
    ...

    def generate_auth_token(self, expires_in = 600):
        exp_timestamp = int(datetime.now(timezone.utc).timestamp()) + expires_in
        return jwt_encode(
            { 'id': self.id, 'exp': exp_timestamp },
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )
```

``` json
{
  "duration": 600,
  "token": "eyJhbGciOiJIUzI1NiIaaaa5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNzaaaakzMDY5fQ.3Qs4_YqgzF9V7mJthr6BYYLiSZDaaaa72zhcc8sI6zQ"
}
```

### UPDATE

Die PATCH-Route dient dem editieren eines Users. Mann kann jegliche Attribute des Users ändern, bis auf die User-ID.

Wichtig zu erwähnen ist, dass auch nur einzelne Aittribute angegeben werden können. Falls ein Attribut fehlt, wird dies schlicht und einfach nicht angepasst.

``` python
class UsersIn(Schema):
    name = String(required=True, validate=Length(0, 128))
    email = String(required=True, validate=[Length(0, 128), Email()])
    password = String(required=True, validate=Length(0, 256))
    is_admin = Boolean(required=False, load_default=False)
```

### DELETE

Die DELETE-Route ist selbsterklärend. Mit ihr kann man einen User anhand der User ID löschen. Es werden keine weiteren Attribute benötigt ausser der User ID.
