import os
import re
class Config:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "mystrikeplans@gmail.com"
    MAIL_PASSWORD = "1122dammy"
    SECRET_KEY = '1122dammy'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
          SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)


