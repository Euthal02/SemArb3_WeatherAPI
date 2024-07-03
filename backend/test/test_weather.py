from test import client

EINSIEDELN_LATTITUDE = "47.1268265"
EINSIEDELN_LONGITUDE = "8.7507869"

def test_make_relay_api_call_based_on_lat_and_lon_without_login(client):
    response = client.get(f"/weather/lookup?lattitude={EINSIEDELN_LATTITUDE}&longitude={EINSIEDELN_LONGITUDE}")
    # here i am looking into the response, to see if it contains the proper response.
    assert isinstance(response.json, dict)
    assert "Unauthorized" in response.json["message"]

def test_make_relay_api_call_based_on_lat_and_lon_with_login(client):
    response0 = client.post("/users/login", json={'email': 'test@test.ch', 'password': 'test'})
    access_token = response0.json["token"]
    headers = {'Authorization': 'Bearer {}'.format(access_token)}

    response = client.get(f"/weather/lookup?lattitude={EINSIEDELN_LATTITUDE}&longitude={EINSIEDELN_LONGITUDE}", headers=headers)
    # here i am looking into the response, to see if it contains the proper response.
    assert isinstance(response.json, dict)
    assert "Einsiedeln" in response.json["city_name"] and "CH" in response.json["country_code"]
