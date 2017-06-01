import os
import os.path
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
basedir = os.path.abspath(os.path.dirname(__file__))
# STATICFILES_DIRS = (
#     os.path.join(basedir, 'ABCSystem/static'),
# )

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    HOST = '127.0.0.1'
    PORT = 8080
    SECRET_KEY = 'change-key-should-be-made'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    LOG_LEVEL="DEBUG"


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