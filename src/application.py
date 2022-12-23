from flask import Flask, Response, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_cors import CORS
from middleware.security import Security
from functools import wraps

db = SQLAlchemy()
# Create the Flask application object.
security = Security()
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:WHQ21cd1c689742@userdb.cyww6g5eerrg.us-east-1.rds.amazonaws.com:3306/user_database?charset=utf8"
app.secret_key = "27eduCBA09"
db.init_app(app)

class User(db.Model):
    __tablename__ = "user_info"
    userId = db.Column('uid', db.Integer, primary_key=True)
    lastName = db.Column('last_name', db.String(100))
    firstName = db.Column('first_name', db.String(100))
    middleName = db.Column('middle_name', db.String(100))
    phone = db.Column('phone', db.String(200))
    email = db.Column('email', db.String(200))
    pwd = db.Column('pwd', db.String(200))
    image = db.Column('image', db.String(200))

    def __init__(self, last_name, first_name, middle_name, phone, email, pwd, image):
        self.lastName = last_name
        self.firstName = first_name
        self.middleName = middle_name
        self.phone = phone
        self.email = email
        self.pwd = pwd
        self.image = image

    def toJson(self):
        return {
            'userId': self.userId,
            'lastName': self.lastName,
            'firstName': self.firstName,
            'middleName': self.middleName,
            'phone': self.phone,
            'email': self.email,
            'image': self.image
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
        last_name, first_name, middle_name, phone, image, email, pwd, confirmedPwd = request.json['last_name'], \
                                                        request.json['first_name'], request.json['middle_name'], request.json['phone'],\
                                                        request.json['image'], request.json['email'], request.json['pwd'],\
                                                        request.json['confirmed_pwd']
        if pwd != confirmedPwd:
            result = Response("password not matched", status=500, content_type="application.json")
            return result
        else:
            hased_pwd = security.hash_password({"pwd": pwd})
            user = User(last_name, first_name, middle_name, phone, email, hased_pwd, image)
            db.session.add(user)
            db.session.commit()
            result = Response("success", status=200, content_type="application.json")
            return result
    except Exception as e:
        print(e)
        result = Response("register failed for some reason", status=500, content_type="application.json")
        return result

@app.route("/api/user/login", methods=["POST"])
def login():
    try:
        email, pwd = request.json['email'], request.json['pwd']
        hased_pwd = security.hash_password({"pwd": pwd})
        user = User.query.filter(User.email == email).first()
        if user:
            if user.pwd == hased_pwd:
                result = Response("login success", status=200, content_type="application.json")
                session["user session"] = user.userId
                print(session)
            else:
                result = Response("invalid password", status=500, content_type="application.json")
        else:
            result = Response("email hasn't been registered", status=500, content_type="application.json")
        return result
    except Exception as e:
        print(e)
        result = Response("login failed", status=500, content_type="application.json")
        return result

@app.route("/api/user/logout")
def logout():
    session.pop("user session", None)
    result = Response("logout success", status=200, content_type="application.json")
    print(session)
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

@app.route("/api/user/checklogin", methods=["GET"])
def checkLogin():
    if "user session" in session:
        result = Response(str(session["user session"]), status=200, content_type="application.json")
        return result
    else:
        return Response("not log in", status=500, content_type="application.json")

@app.route("/api/user/update", methods=["POST"])
def updateById():
    try:
        uid = request.json['uid']
        if 'user session' in session and session['user session'] == int(uid):
            last_name, first_name, middle_name, phone, image, email, pwd, confirmedPwd = request.json['last_name'], \
                                                        request.json['first_name'], request.json['middle_name'], request.json['phone'],\
                                                        request.json['image'], request.json['email'], request.json['pwd'],\
                                                        request.json['confirmed_pwd']
            user = User.query.filter(User.userId == uid).first()
            if pwd != confirmedPwd:
                result = Response("password not matched", status=500, content_type="application.json")
                return result
            else:
                user.lastName = last_name
                user.firstName = first_name
                user.middleName = middle_name
                user.phone = phone
                user.image = image
                user.email = email
                user.pwd = pwd
                print(user)
                db.session.add(user)
                db.session.commit()
                result = Response("update success", status=200, content_type="application.json")
                return result
        else:
            result = Response("update failed, not login", status=500, content_type="application.json")
            print(session)
            return result
    except Exception as e:
        print(e)
        result = Response("update failed for some reason", status=500, content_type="application.json")
        return result

@app.route("/api/user/delete/<uid>", methods=['DELETE'])
def deleteUser(uid):
    try:
        user = User.query.filter(User.userId == uid)
        print(user)
        unt = user.delete()
        db.session.commit()
        ret = dict(success=True, cnt=unt)
        return ret
    except Exception as e:
        print(e)
        ret = dict(success=False)
        return ret

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)