from app import app, engine
from flask import render_template, redirect, request, session, flash, url_for
from sqlalchemy.orm import sessionmaker
from .models import User, Appointment, AppointmentDate, AppointmentTime, Subscription
import datetime

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
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
            flash(u'Invalid login or password.', 'danger')
        return redirect(url_for('main'))
    else:
        if session.get('logged_in'):
            flash(u'You have already logged in.', 'info')
            return redirect(url_for('main'))
        return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash(u'Signed out successfully.', 'success')
    return redirect(url_for('main'))

@app.route('/appointment/<int:id>')
def appointment(id):
    Session = sessionmaker(bind=engine)
    s = Session()
    appointment = s.query(Appointment).filter_by(id=id).first()
    appointment_dates = s.query(AppointmentDate) \
        .filter(id==AppointmentDate.appointment_id).all()
    appointment_times = s.query(AppointmentTime) \
        .filter(id==AppointmentTime.appointment_id).all()

    return render_template('appointment.html',
                            appointment=appointment,
                            dates=appointment_dates,
                            times=appointment_times)

@app.route('/subscription', methods=['GET', 'POST'])
def subscription():
    if request.method == 'POST':
        post_fullname = request.form['fullname']
        post_email = request.form['email']
        post_date = int(request.form['dates'])
        post_time = int(request.form['times'])
        post_appointment = int(request.form['appointment'])
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(Subscription).filter_by(
            fullname=post_fullname,
            email=post_email,
            appointment_id=post_appointment
        ).first()
        if query:
            flash(u'You already have a subscription.', 'warning')
        else:
            sub = Subscription(post_fullname, post_email, post_appointment, 
                                post_date, post_time)
            s.add(sub)
            s.commit()
            flash(u'Sucessfully subscribed.', 'success')
        return redirect(url_for('main'))

@app.route('/addnumbers', methods=['GET', 'POST'])
def add_numbers():
    if request.method == 'POST':
        dates_number = int(request.form['date'])
        times_number = int(request.form['time'])
        return render_template('add_appoint.html',
                                dates=dates_number,
                                times=times_number)
    else:
        if session.get('logged_in'):
            return render_template('add_numbers.html')
        else:
            flash(u'You must to login first.', 'danger')
            return redirect(url_for('main'))

@app.route('/addappoint', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        date_numbers = int(request.form['dates_n'])
        time_numbers = int(request.form['times_n'])
        appoint_name = request.form['appoint_name']
        Session = sessionmaker(bind=engine)
        s = Session()
        appoint = Appointment(appoint_name)
        s.add(appoint)
        s.flush()
        appoint_id = appoint.id
        
        dates = []
        times = []
        for i in range(1, date_numbers+1):
            date = datetime.datetime.strptime(request.form[str(i)], "%Y-%m-%d")
            d = AppointmentDate(date.date(), appoint_id)
            dates.append(d)
        for i in range(1, time_numbers+1):
            start = datetime.datetime.strptime(request.form[str(i)+'_start'], "%H:%M")
            end = datetime.datetime.strptime(request.form[str(i)+'_end'], "%H:%M")
            start = start.time()
            end = end.time()
            time = AppointmentTime(start, end, appoint_id)
            times.append(time)
        s.add_all(dates)
        s.add_all(times)
        s.commit()
        flash(u'Sucessfully added a new appointment.', 'success')
        return redirect(url_for('main'))
    else:
        if session.get('logged_in'):
            return render_template('add_appoint.html')
        else:
            flash(u'You must to login first.', 'warning')
            return redirect(url_for('main'))
