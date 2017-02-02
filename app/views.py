from app import app, engine
from flask import render_template, redirect, request, session, flash, url_for
from sqlalchemy.orm import sessionmaker
from .models import User, Appointment

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/appointments')
def main():
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Appointment).all()
    return render_template('appointments.html', appoints=query)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User).filter(User.username.in_ \
            ([username]), User.password.in_([password])).first()

        if query:
            session['logged_in'] = True
            session['user'] = username
        else:
            flash('Invalid login or password.')
        return redirect(url_for('main'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('Signed out successfully.')
    return redirect(url_for('main'))

