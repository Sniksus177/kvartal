import hashlib
import secrets

_users = {}
_next_id = 1

def make_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 200000).hex()

def create_user(name, email, password):
    global _next_id
    email = email.lower().strip()
    if email in _users:
        return None
    salt = secrets.token_hex(16)
    user = {"id": _next_id, "name": name, "email": email, "password_hash": make_password(password, salt), "salt": salt}
    _users[email] = user
    _next_id += 1
    return user["id"]

def get_user_by_email(email):
    user = _users.get(email.lower().strip())
    return dict(user) if user else None

def get_user_by_id(user_id):
    for user in _users.values():
        if user["id"] == user_id:
            return {"id": user["id"], "name": user["name"], "email": user["email"]}
    return None

def check_user_password(user, password):
    if not user:
        return False
    return secrets.compare_digest(make_password(password, user["salt"]), user["password_hash"])
