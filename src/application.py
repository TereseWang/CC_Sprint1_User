from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_cors import CORS

db = SQLAlchemy()
# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:dbuserdbuser@ccprojectuser.coxdk1mcsnw2.us-east-1.rds.amazonaws.com/user_database?charset=utf8"

db.init_app(app)


class User(db.Model):
    __tablename__ = "user_info"
    userId = db.Column('uid', db.Integer, primary_key=True)
    lastName = db.Column('last_name', db.String(100))
    firstName = db.Column('first_name', db.String(100))
    middleName = db.Column('middle_name', db.String(100))
    phone = db.Column(db.String(200))
    email = db.Column(db.String(200))
    pwd = db.Column(db.String(200))

    def __init__(self, last_name, first_name, middle_name, phone, email, pwd):
        self.lastName = last_name
        self.firstName = first_name
        self.middleName = middle_name
        self.phone = phone
        self.email = email
        self.pwd = pwd

    def toJson(self):
        return {
            'userId': self.userId,
            'lastName': self.lastName,
            'firstName': self.firstName,
            'middleName': self.middleName,
            'phone': self.phone,
            'email': self.email
        }


@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "User-Microservice",
        "health": "Good",
        "at time": t
    }

    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


@app.route("/api/user/register", methods=["POST"])
def register():
    try:
        lastName, firstName, middleName, phone, email, pwd, confirmedPwd = request.json['lastName'], request.json['firstName'], \
                                                             request.json['middleName'], request.json['phone'], request.json['email'], request.json['password'], request.json['confirmedPassword']
        user = User(lastName, firstName, middleName, phone, email, pwd)
        db.session.add(user)
        db.session.commit()
        result = Response("success", status=200, content_type="application.json")
        return result
    except Exception as e:
        result = Response("register failed", status=500, content_type="application.json")
        return result


@app.route("/api/user/login", methods=["POST"])
def login():
    try:
        email, pwd = request.json['email'], request.json['password']
        user = User.query.filter(User.email == email).first()
        print(user)
        if user:
            if user.pwd == pwd:
                result = Response("success", status=200, content_type="application.json")
            else:
                result = Response("invalid password", status=500, content_type="application.json")
        else:
            result = Response("email hasn't been registered", status=500, content_type="application.json")

        return result
    except Exception as e:
        print(e)
        result = Response("register failed", status=500, content_type="application.json")
        return result


@app.route("/api/user/info/<uid>", methods=["GET"])
def getUserInfo(uid):
    try:
        user = User.query.filter(User.userId == uid).first()
        print(user)
        if user:
            msg = user.toJson()
            result = Response(json.dumps(msg), status=200, content_type="application.json")
        else:
            result = Response("userId cannot be found", status=500, content_type="application.json")
        return result
    except Exception as e:
        print(e)
        result = Response("getUserInfo failed", status=500, content_type="application.json")
        return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)

