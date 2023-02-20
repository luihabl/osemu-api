import os

def _get_db_uri(**kwargs):
    
    db_data = {
        'db_user': os.environ.get('POSTGRES_USER'),
        'db_pass': os.environ.get('POSTGRES_PASSWORD'),
        'db_name': os.environ.get('POSTGRES_DB'),
        'db_host': os.environ.get('POSTGRES_HOST')
    }

    db_data.update(kwargs)

    return f'postgresql+psycopg2://{db_data["db_user"]}:{db_data["db_pass"]}@{db_data["db_host"]}/{db_data["db_name"]}'


class BaseConfig:
    TESTING = False
    SQLALCHEMY_DATABASE_URI = _get_db_uri()
    

class DevelopmentConfig(BaseConfig):
    SECRET_KEY=os.environ.get('FLASK_DEV_SECRET_KEY')


class TestingConfig(DevelopmentConfig):
    TESTING = True
