import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    user = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    host = os.environ['POSTGRES_HOST']
    database = os.environ['POSTGRES_DB']
    port = os.environ['POSTGRES_PORT']

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    SECRET_KEY = '2a0f51a5c1992df84ee9bbd9817492d5'