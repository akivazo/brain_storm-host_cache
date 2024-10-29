import pytest
from flask import Flask
from flask.testing import FlaskClient
from mongomock import MongoClient
from ..cache_api import server, set_mongo_client

@pytest.fixture
def client():
    # Create a mock MongoDB client
    mock_mongo_client = MongoClient()
    set_mongo_client(mock_mongo_client)
    server.config['TESTING'] = True
    # Set up Flask test client
    client = server.test_client()
    yield client
    mock_mongo_client.close()

def test_add_host(client: FlaskClient):
    response = client.post("/host_cache", json={"host": "MyMachin", "name": "John Doe", "password": "bla"})

    assert response.status_code == 201

def test_get_host(client: FlaskClient):
    response = client.post("/host_cache", json={"host": "MyMachin", "name": "John Doe", "password": "bla"})
    response = client.post("/host_cache", json={"host": "MyMachin2", "name": "John Doe2", "password": "bla2"})

    assert response.status_code == 201

    response = client.get("/host_cache/MyMachin")

    assert response.status_code == 200

    json = response.get_json()

    assert json == {"host": "MyMachin", "name": "John Doe", "password": "bla"}

def test_not_exist(client: FlaskClient):
    response = client.get("/host_cache/NotExistMachin")

    assert response.status_code == 404

def test_update_host(client: FlaskClient):
    response = client.post("/host_cache", json={"host": "MyMachin", "name": "John Doe", "password": "bla"})

    assert response.status_code == 201

    response = client.get("/host_cache/MyMachin")

    assert response.status_code == 200

    json = response.get_json()

    assert json == {"host": "MyMachin", "name": "John Doe", "password": "bla"}

    response = client.post("/host_cache", json={"host": "MyMachin", "name": "Eli Moshonov", "password": "blabla"})

    response = client.get("/host_cache/MyMachin")

    assert response.status_code == 200

    json = response.get_json()

    assert json == {"host": "MyMachin", "name": "Eli Moshonov", "password": "blabla"}

