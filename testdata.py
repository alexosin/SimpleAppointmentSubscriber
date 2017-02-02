from app import engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Appointment, AppointmentDate, AppointmentTime
import datetime

Session = sessionmaker(bind=engine)
session = Session()

session.add_all([
    User('admin', 'password'),
    User('1', '1'),
    Appointment('First'),
    Appointment('Second'),
    AppointmentDate(date=datetime.date(2017, 3, 1), appointment_id=1),
    AppointmentDate(date=datetime.date(2017, 3, 3), appointment_id=1),
    AppointmentDate(date=datetime.date(2017, 3, 20), appointment_id=2),
    AppointmentTime(start=datetime.time(10), end=datetime.time(11), appointment_id=1),
    AppointmentTime(start=datetime.time(20), end=datetime.time(21), appointment_id=2)
])

session.commit()
