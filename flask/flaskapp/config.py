import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    user = os.getenv('POSTGRES_USER', 'postgres')
    password = os.getenv('POSTGRES_PASSWORD', 'postgres')
    host = os.getenv('POSTGRES_HOST', 'localhost')
    database = os.getenv('POSTGRES_DB', 'postgres')
    port = os.getenv('POSTGRES_PORT', 5432)

    # SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
    SECRET_KEY = '2a0f51a5c1992df84ee9bbd9817492d5'

    MAIL_SERVER ='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'galimentisrl@gmail.com'
    MAIL_PASSWORD = 'prova_123'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True