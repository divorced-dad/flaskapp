from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object("flaskapp.config.Config")
# app.config['SECRET_KEY'] = '2a0f51a5c1992df84ee9bbd9817492d5'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/beni_primari'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://test:test@0.0.0.0:5401/test'
                                    # 'postgresql://postgres:postgres@localhost:5432/postgres'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'



from flaskapp import routes