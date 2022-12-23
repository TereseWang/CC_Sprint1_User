import jwt

class Security():
    def hash_password(self, pwd):
        h = jwt.encode(pwd, key="secret")
        h = str(h)
        return h