from flask.cli import FlaskGroup

from app import app
from app.model import db, User


cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    db.session.add(User(
        dni="10069402",
        email="isa@correo.com",
        password="IsaPass",
        name="Isabella Gomez",
        role="admin",
        ))
    db.session.commit()

if __name__ == "__main__":
    cli()