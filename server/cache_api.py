from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pydantic import BaseModel, Field, ValidationError
from typing import Type, List

class HostCache(BaseModel):
    name: str
    password: str
    host: str


server = Flask(__name__)
CORS(server)
user_cache_collection = None

def set_mongo_client(mongo_client: MongoClient):
    global user_cache_collection
    user_cache_collection = mongo_client.get_database("brain_storm").get_collection("host_cache")

@server.route("/")
def root():
    return "Host cache Api"

def validate_json_schema(json: dict, cls: Type):
    # validate that the accepted json is containing all the data nedded
    instance = None
    try:
        instance = cls(**json)
    except ValidationError as e:
        return None, e.json()
    return instance.__dict__, ""


@server.route("/host_cache", methods=["POST"])
def add_host_cache():
    data = request.get_json()
    instance, error_message = validate_json_schema(data, HostCache)
    if not instance:
        return jsonify({"error": error_message}), 400
    # check if exist
    host = instance["host"]
    user_cache_collection.update_one({"host": host}, {"$set": instance}, upsert=True)
    return jsonify("Host Cache Updated Succesfully"), 201

@server.route("/host_cache/<host>", methods=["GET"])
def get_host_cache(host):
    result = user_cache_collection.find_one({"host": host}, {"_id": 0})
    if result is None:
        return jsonify(f"Host {host} were not found"), 404
    return jsonify(result), 200