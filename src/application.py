from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from user_resource import UserResource
from flask_cors import CORS

db = SQLAlchemy()
# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://chole:@localhost:3306/user_database?charset=utf8"
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
            'userId': self.uid,
            'lastName': self.last_name,
            'firstName': self.first_name,
            'middleName': self.middle_name,
            'phone': self.phone,
            'email': self.email
        }


@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "F22-Starter-Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


@app.route("/api/user/register", methods=["POST"])
def register():
    try:
        print("ok")
        lastName, firstName, middleName, phone, email, pwd, confirmedPwd = request.json['lastName'], request.json['firstName'], \
                                                             request.json['middleName'], request.json['phone'], request.json['email'], request.json['password'], request.json['confirmedPassword']

        print(lastName)
        user = User(lastName, firstName, middleName, phone, email, pwd)
        db.session.add(user)
        db.session.commit()
        ret = dict(success=True)
        return ret
    except Exception as e:
        print(e)
        ret = dict(success=False)
        return ret



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)

