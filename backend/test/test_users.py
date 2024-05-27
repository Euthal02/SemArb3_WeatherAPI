from test import client

def test_get_users_without_authentication(client):
    response = client.get("/users/")
    # test if this is unauthorized, which is good, this means authentication works.
    assert response.status_code == 401

def test_get_users_with_wrong_authentication(client):
    # this also tests the login function.
    response0 = client.post("/users/login", json={'email': 'test@test.ch', 'password': 'falschespassword'})
    # test if this is unauthorized, which is good, this means the auth request was denied.
    assert response0.status_code == 401

def test_get_users_with_authentication(client):
    # this also tests the login function.
    response0 = client.post("/users/login", json={'email': 'test@test.ch', 'password': 'test'})
    access_token = response0.json["token"]
    headers = { 'Authorization': 'Bearer {}'.format(access_token) }

    response = client.get("/users/", headers=headers)
    # here i am looking into the response, to see if it contains the proper response.
    assert isinstance(response.json, list)
    assert isinstance(response.json[0], dict)
    assert "id" in response.json[0].keys()

def test_get_users_with_specific_id(client):
    # this also tests the login function.
    response0 = client.post("/users/login", json={'email': 'test@test.ch', 'password': 'test'})
    access_token = response0.json["token"]
    headers = { 'Authorization': 'Bearer {}'.format(access_token) }

    response = client.get("/users/1", headers=headers)
    # here i am looking into the response, to see if it contains the proper response.
    assert isinstance(response.json, dict)
    assert "id" in response.json.keys()

def test_create_a_new_user(client):
    response0 = client.post("/users/login", json={'email': 'test@test.ch', 'password': 'test'})
    access_token = response0.json["token"]
    headers = { 'Authorization': 'Bearer {}'.format(access_token) }

    #create user incorrectly. missing name field.
    response1 = client.post("/users/create", json={'email': 'neuer@user.ch', 'password': 'neueruser'}, headers=headers)
    # here i am looking into the response, to see if it contains the proper response.
    assert isinstance(response1.json, dict)
    assert 'Validation error' in response1.json['message']

    # create user correctly
    response2 = client.post("/users/create", json={'name': 'emil', 'email': 'neuer@user.ch', 'password': 'neueruser'}, headers=headers)
    # here i am looking into the response, to see if it contains the proper response.
    assert isinstance(response2.json, dict)
    assert "emil" in response2.json["name"]

def test_edit_user(client):
    response0 = client.post("/users/login", json={'email': 'test@test.ch', 'password': 'test'})
    access_token = response0.json["token"]
    headers = { 'Authorization': 'Bearer {}'.format(access_token) }
    client.post("/users/create", json={'name': 'emil', 'email': 'neuer@user.ch', 'password': 'neueruser'}, headers=headers)

    # with wrong id
    response1 = client.patch("/users/3/edit", json={'name': 'josef'}, headers=headers)
    assert response1.status_code == 404

    # with correct id
    response2 = client.patch("/users/2/edit", json={'name': 'josef'}, headers=headers)
    assert isinstance(response2.json, dict)
    assert "josef" in response2.json["name"]

def test_delete_user(client):
    # this also tests the login function.
    response0 = client.post("/users/login", json={'email': 'test@test.ch', 'password': 'test'})
    access_token = response0.json["token"]
    headers = { 'Authorization': 'Bearer {}'.format(access_token) }
    client.post("/users/create", json={'name': 'emil', 'email': 'neuer@user.ch', 'password': 'neueruser'}, headers=headers)

    # wrong id
    response1 = client.delete("/users/3/delete", headers=headers)
    # here i am looking into the response, to see if it contains the proper response.
    assert response1.status_code == 404

    # correct id
    response2 = client.delete("/users/2/delete", headers=headers)
    all_remaining_user_ids = []
    for user in response2.json:
        all_remaining_user_ids.append(user["id"])
    assert 2 not in all_remaining_user_ids
