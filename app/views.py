from flask import Flask, request, session, redirect, url_for, render_template, flash
from urllib.parse import parse_qs, urlparse, urlunparse
from .models import Person, list_all_people, list_all_locations
import os



def create_app():
    app = Flask(__name__)
    return app

app=create_app()
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET','POST'])
def index():
    p = list_all_people()
    l = list_all_locations()
    return render_template('index.html', people=p, locations=l)


@app.route('/person/info', methods=['GET','POST'])
def info_person():
    url = urlparse(request.url)
    name = parse_qs(url.query)['name'][0]
    person = Person(name)
    # residentcity = person.get_birthplace()
    # friends = person.get_friends()
    # return render_template('info_person.html', name = name, residentcity = residentcity, friends = friends)
    return render_template('info_person.html', name = name)


@app.route('/person/add', methods=['GET','POST'])
def add_person():
    if request.method == 'POST':
        name = request.form['name']
        if not Person(name).add():
            flash('Person with this name exist in database')
        else:
            return redirect(url_for('index'))
    return render_template('add_person.html')


@app.route('/person/delete', methods=['GET','POST'])
def delete_person():
    if request.method == 'POST':
        name = request.form['name']
        Person(name).delete()
        return redirect(url_for('index'))

    p = list_all_people()
    return render_template('delete_person.html', people = p)