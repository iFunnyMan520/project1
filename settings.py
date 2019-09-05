from flask_sqlalchemy import SQLAlchemy


class DevelopmentConfig:

    def __init__(self):
        self.db = SQLAlchemy()
        self.db_session = self.db.session

    ENV = 'development'
    DEBUG = True
    DB_PATH = 'test.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret_key'


config = DevelopmentConfig()
db = config.db
