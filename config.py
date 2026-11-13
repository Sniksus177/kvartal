import os
import hashlib
import secrets


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-before-publishing")
    ADMIN_LOGIN = os.getenv("ADMIN_LOGIN", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
    ADMIN_PASSWORD_HASH = hashlib.pbkdf2_hmac(
        "sha256",
        ADMIN_PASSWORD.encode("utf-8"),
        b"kvartal-admin",
        200000
    )


def check_admin_password(password):
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        b"kvartal-admin",
        200000
    )
    return secrets.compare_digest(password_hash, Config.ADMIN_PASSWORD_HASH)
