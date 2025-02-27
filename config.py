import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://user:password@localhost/hospital_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

