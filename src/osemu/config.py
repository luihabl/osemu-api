import os

def _get_db_uri(**kwargs):
    
    db_data = {
        'db_user': os.environ.get('POSTGRES_USER'),
        'db_pass': os.environ.get('POSTGRES_PASSWORD'),
        'db_name': os.environ.get('APP_DB'),
        'db_host': os.environ.get('POSTGRES_HOST'),
        'db_port': os.environ.get('POSTGRES_PORT')
    }

    db_data.update(kwargs)

    return f'postgresql+psycopg2://{db_data["db_user"]}:{db_data["db_pass"]}@{db_data["db_host"]}:{db_data["db_port"]}/{db_data["db_name"]}'


class BaseConfig:
    TESTING = False
    SQLALCHEMY_DATABASE_URI = _get_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'sandstone'
    CORS_HEADERS = 'Content-Type'
    START_SCHEDULED_JOBS=True

class Config(BaseConfig):
    SECRET_KEY=os.environ.get('FLASK_SECRET_KEY')

class ConfigNoScheduledJobs(Config):
    START_SCHEDULED_JOBS=False

class TestingConfig(ConfigNoScheduledJobs):
    TESTING = True
