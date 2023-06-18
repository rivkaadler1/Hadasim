import os
from flask import Flask, Response, request, jsonify, make_response
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.json_util import dumps

load_dotenv()

app = Flask(__name__)

mongo_db_url = os.environ.get("MONGO_DB_CONN_STRING")
client = MongoClient(mongo_db_url)
db = client['members_db']


class APIError(Exception):
    """All custom API Exceptions"""
    pass


@app.get("/api/members")
def get_members():
    member_id = request.args.get('member_id')
    members_filter = {} if member_id is None else {"member_id": member_id}
    members = list(db.members.find(members_filter))

    response = Response(
        response=dumps(members), status=200, mimetype="application/json")
    return response


class APIBadReqError(APIError):
    """Custom Bad Request Error Class."""
    code = 400
    description = "Bad Request error"


@app.errorhandler(APIError)
def handle_exception(err):
    """Return custom JSON when APIError or its children are raised"""
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]
    return jsonify(response), err.code


def check_input(_json):
    required_fields = ["first_name", "last_name", "address", "date_of_birth", "telephone", "mobile_phone",
                       "vaccine_dates",
                       "vaccine_manufacturers", "member_id"]
    if not all(field in _json for field in required_fields):
        raise APIBadReqError("Missing required fields")

    if not all(key in _json["address"] for key in ("city", "street", "number")):
        raise APIBadReqError("Bad request - address field must include city, street, and number")

    if len(_json["member_id"]) != 9:
        raise APIBadReqError("Bad id number")

    # Check if member_id already exists in the database
    existing_member = db.members.find_one({"member_id": _json["member_id"]})
    if existing_member:
        raise APIBadReqError("Member with the same ID already exists")

    if not isinstance(_json["vaccine_dates"], list) or not isinstance(_json["vaccine_manufacturers"], list):
        raise APIBadReqError("The type of the fields :vaccine_dates,vaccine_manufacturers should be list")

    if len(_json["vaccine_dates"]) != len(_json["vaccine_manufacturers"]):
        raise APIBadReqError("The number of vaccination dates is not the same as the number of their manufacturers"
                             " - incompatibility.")

    if len(_json["vaccine_dates"]) > 4:
        raise APIBadReqError("The number of vaccination dates is more than 4")


@app.post("/api/members")
def add_member():
    _json = request.json
    check_input(_json)
    db.members.insert_one(_json)
    resp = jsonify({"message": "Member added successfully"})
    resp.status_code = 201
    return resp


@app.errorhandler(404)
def handle_404_error(error):
    return make_response(jsonify({"errorCode": error.code,
                                  "errorDescription": "Resource not found!",
                                  "errorDetailedDescription": error.description,
                                  "errorName": error.name}), 404)


@app.errorhandler(500)
def handle_500_error(error):
    return make_response(jsonify({"errorCode": error.code,
                                  "errorDescription": "Internal Server Error",
                                  "errorDetailedDescription": error.description,
                                  "errorName": error.name}), 500)


if __name__ == "__main__":
    app.run()
