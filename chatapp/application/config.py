import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # sqlite
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

    # postgres
    #SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='postgres',pw='mysecretpassword',url='localhost',db='postgres')

    # mysql
    SQLALCHEMY_DATABASE_URI = f'mysql://{os.environ.get("MYSQL_DBNAME", default = "root")}:{os.environ.get("MYSQL_PASSWORD")}@{os.environ.get("MYSQL_host",default="localhost")}/chatapp'

    # Google OAuth2 configuration
    GOOGLE_CLIENT_ID = os.environ.get ("GOOGLE_CLIENT_ID" , None)
    GOOGLE_CLIENT_SECRET = os.environ.get ("GOOGLE_CLIENT_SECRET" , None)
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True