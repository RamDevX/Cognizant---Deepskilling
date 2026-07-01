import os

class Config:
    SECRET_KEY = "hands_on_5_secret_key"

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:####$@localhost/course_management_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False