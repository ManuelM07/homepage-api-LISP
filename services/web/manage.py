from flask.cli import FlaskGroup
from app.model import db, User, app, Zone


cli = FlaskGroup(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
        active=True
        ))
    db.session.commit()


@cli.command("create_zones")
def create_zones():
    db.session.add(Zone(
        name="Complexes zone",
        description=
        """Morbi pharetra blandit mi, varius tempus turpis condimentum sed. 
        Vestibulum ante ipsum primis in faucibus orci luctus et ultrices 
        posuere cubilia curae; In eu quam vitae neque consequat imperdiet. 
        Praesent consequat tincidunt feugiat. Sed auctor cursus ipsum eu mollis. 
        Phasellus non risus ut quam tristique malesuada et sit amet dolor.""",
    ))   
    db.session.add(Zone(
        name="Medical service",
        description=
        """Morbi pharetra blandit mi, varius tempus turpis condimentum sed. 
        Vestibulum ante ipsum primis in faucibus orci luctus et ultrices 
        posuere cubilia curae; In eu quam vitae neque consequat imperdiet. 
        Praesent consequat tincidunt feugiat. Sed auctor cursus ipsum eu mollis. 
        Phasellus non risus ut quam tristique malesuada et sit amet dolor.""",
    ))
    db.session.commit()  

if __name__ == "__main__":
    cli()