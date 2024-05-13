from test import client

def test_get_students(client):
    response0 = client.post("/users/login", json={'email': 'test@test.ch', 'password': 'test'})
    access_token = response0.json["token"]
    headers = { 'Authorization': 'Bearer {}'.format(access_token) }

    response = client.get("/students/", headers=headers)
    assert response.json[4]['name'] == 'Mega Tron'

def test_post_student(client):
    response0 = client.post("/users/login", json={'email': 'test@test.ch', 'password': 'test'})
    access_token = response0.json["token"]
    headers = { 'Authorization': 'Bearer {}'.format(access_token) }
    
    response = client.post("/students/create", json={
            'name': 'Nina Hagen', 'level': 'AP'
        }, headers=headers)
    assert response.status_code == 201

