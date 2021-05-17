## Installation

### venv
- activate venv
    venv\Scripts\activate

### pip install

- Flask
    pip install Flask
- Flask WT Forms
    pip install flask_wtf
    pip install email_validator
    pip install wtforms_components
- Flask SQLAlchemy ORM
    pip install flask-sqlalchemy
- Mysql
    pip install mysqlclient
- Flask bcrypt hashing algorithm
    pip install flask-bcrypt
- Flask login
    pip install flask-login


### database 

- creare un db mysql
- modificare opportunamente la stringa di connessione
    `# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/beni_primari'`

## Dev Run

"""
cd project-folder

py run.py
"""