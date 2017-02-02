from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User(id {}, username {}, password {})>' \
                            .format(self.id, self.username, self.password)

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    appointment_date = relationship('AppointmentDate', backref='appointments')
    appointment_time = relationship('AppointmentTime', backref='appointments')
    subs = relationship('Subscription', backref='appointments')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Appointment(id {}, name {})>".format(self.id, self.name)

class AppointmentDate(Base):
    __tablename__ = "appointment_dates"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    appointment_id = Column(Integer, ForeignKey('appointments.id'))
    subs = relationship('Subscription', backref='appointment_dates')

    def __init__(self, date, appointment_id):
        self.date = date
        self.appointment_id = appointment_id

    def __repr__(self):
        return '<AppointmentDate(id {}, date {}, appointment {})>' \
            .format(self.id, self.date, self.appointment_id)

class AppointmentTime(Base):
    __tablename__ = "appointment_times"

    id = Column(Integer, primary_key=True)
    start = Column(Time)
    end = Column(Time)
    appointment_id = Column(Integer, ForeignKey('appointments.id'))
    subs = relationship('Subscription', backref='appointment_times')

    def __init__(self, start, end, appointment_id):
        self.start = start
        self.end = end
        self.appointment_id = appointment_id
    
    def __repr__(self):
        return '<AppointmentTime(id {}, start {}, end {}, appointment {})>' \
            .format(self.id, self.start, self.end, self.appointment_id)

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    fullname = Column(String)
    email = Column(String)
    appointment_id = Column(Integer, ForeignKey('appointments.id'))
    appointment_date = Column(Integer, ForeignKey('appointment_dates.id'))
    appointment_time = Column(Integer, ForeignKey('appointment_times.id'))

    def __init__(self, fullname, email, appointment_id, appointment_date, appointment_time):
        self.fullname = fullname
        self.email = email
        self.appointment_id = appointment_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
    
    def __repr__(self):
        return '<Subscription(id {}, fullname {}, email {}, appointment_id {})>' \
            .format(self.id, self.fullname, self.email, self.appointment_id)

if __name__=='__main__':
    engine = create_engine('sqlite:///app.db', echo=True)
    Base.metadata.create_all(engine)
