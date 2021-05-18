from flaskapp import app, db
from flask.cli import FlaskGroup


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

# cli = FlaskGroup(create_app=(lambda:app))


# @cli.command("create_db")
# def create_db():
#     db.drop_all()
#     db.create_all()
#     db.session.commit()


# if __name__ == "__main__":
#     cli()