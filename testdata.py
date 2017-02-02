from app import engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Appointment

Session = sessionmaker(bind=engine)
session = Session()

session.add_all([
    User('admin', 'password'),
    User('1', '1'),
    Appointment('First'),
    Appointment('Second')
])

session.commit()
