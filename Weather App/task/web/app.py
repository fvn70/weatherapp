import datetime

import requests
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import sys


dict = {}
key = 'my_key'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SECRET_KEY'] = 'So-Seckrekt'
db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    city_id = db.Column(db.Integer, unique=True, nullable=False)

db.create_all()

def daytime(t):
    return "night" if 22 <= t <= 23 or 0 <= t <= 3 else "day" if 10 <= t <= 17 else "evening-morning"

def get_data(name):
    req = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={name}&units=metric&appid={key}').json()
    if len(req) > 5:
        data = {'city': req['name'],
            'city_id': req['id'],
            'temp': int(req['main']['temp']),
            'state': req['weather'][0]['main'],
            'daytime': daytime((datetime.datetime.utcnow() + datetime.timedelta(seconds=req['timezone'])).hour)}
    else:
        data = None
    return data

def save_data(name):
    req = get_data(name)
    if not req:
        flash("The city doesn't exist!")
    else:
        rec = City.query.filter_by(name=name).first()
        if not rec:
            rec = City(name=name, city_id=req['city_id'])
            db.session.add(rec)
            db.session.commit()
        else:
            flash("The city has already been added to the list!")

def read_data():
    recs = db.session.query(City).all()
    global dict
    dict = {}
    for rec in recs:
        d = get_data(rec.name)
        dict.setdefault('class', []).append(d['daytime'])
        dict.setdefault('degrees', []).append(d['temp'])
        dict.setdefault('state', []).append(d['state'])
        dict.setdefault('city', []).append(d['city'])
        dict.setdefault('city_id', []).append(d['city_id'])

    db.session.commit()

@app.route('/delete/<city_id>', methods=['POST'])
def del_card(city_id):
    City.query.filter_by(city_id=city_id).delete()
    db.session.commit()
    return redirect('/')

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        city_name = request.form['city_name']
        save_data(city_name)
        return redirect('/')
    else:
        read_data()
        num = len(dict['city']) if dict else 0
        return render_template('index.html', weather=dict, card_num=num)

# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
