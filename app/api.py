from app import app, engine
from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from .models import Appointment, Subscription

@app.route('/api/appointments', methods=['GET'])
def get_appoints():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Appointment).all()
    return json.dumps({'appointments': [a.serialize() for a in query]})

@app.route('/api/subscriptions', methods=['GET'])
def get_subs():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Subscription).all()
    return json.dumps({'subscriptions': [s.serialize() for s in query]})
