from datetime import timedelta


class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:237297@localhost:3306/hotel"
    SECRET_KEY = "23424525srwqrq52345"
    PERMANENT_SESSION_LIFETIME = timedelta(days=2)


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"
