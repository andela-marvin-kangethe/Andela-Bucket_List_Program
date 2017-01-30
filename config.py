# # Statement for enabling the development environment
# DEBUG = True

# # Define the application directory
# import os
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# # Define the database - we are working with
# # SQLite for this example
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
# DATABASE_CONNECT_OPTIONS = {}

# SQLALCHEMY_TRACK_MODIFICATIONS = False

# # Secret key for signing cookies
# SECRET_KEY = "secret"



import os

# Define the application directory
base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """ 
     Defined database using Sqlite
    """
    SECRET_KEY = 'm3^f+(c&nq9%jg8a4dc=@@0k8*#pl_-i0=ib@6)^$9drb-v5ba'
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'app.db')

    API_ROOT = 'api/v1'


    @staticmethod
    def init_app(app):
        pass
        
class ProductionConfig(Config):
    """
     This class cofigures the production
     environment properties
    """
    TESTING = True

    DEBUG = False


class StagingConfig(Config):
    """
     This class configures the staging
     environment properties
    """
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """
     This class configures the development
     environment properties
    """
    DEBUG = True

    TESTING = True

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """
     This class cofigures the testing
     environment properties
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'test.db')
    
    DEBUG = True

    TESTING = True

    SERVER_NAME = 'http://127.0.0.1:5000/api/v1'

config = {
    'production': ProductionConfig,
    'staging': StagingConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}