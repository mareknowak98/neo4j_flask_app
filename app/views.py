from flask import Flask, request, session, redirect, url_for, render_template, flash
from urllib.parse import parse_qs, urlparse, urlunparse
from .models import Person, Location, list_all_people, list_all_locations
import os



def create_app():
    app = Flask(__name__)
    return app

app=create_app()
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET','POST'])
def index():
    people = list_all_people()
    locations = list_all_locations()
    return render_template('index.html', people=people, locations=locations)


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


@app.route('/location/add', methods=['GET','POST'])
def add_location():
    if request.method == 'POST':
        city = request.form['city']
        state = request.form['state']
        if not Location(city, state).add():
            flash('City in given voivodeship exist in database!')
        else:
            return redirect(url_for('index'))
    return render_template('add_location.html')


@app.route('/location/delete', methods=['GET','POST'])
def delete_location():
    if request.method == 'POST':
        location = request.form['location']
        l = location.split(",")
        Location(l[0][2:-1], l[1][2:-2]).delete()
        return redirect(url_for('index'))

    loc = list_all_locations()
    return render_template('delete_location.html', locations = loc)


@app.route('/city/info', methods=['GET'])
def info_city():
    url = urlparse(request.url)
    city = parse_qs(url.query)['city'][0]
    state = parse_qs(url.query)['state'][0]
    location = Location(city, state)
    # people_live_in = location.get_people_live_in(city)
    # distances = location.get_dist()
    # dist_dict = {}
    # for elem in distances:
    #     temp1 = elem[1]
    #     temp2 = elem[0][0]['data']['dist']
    #     dist_dict[temp1] = temp2

    # return render_template('info_city.html', city = location, people_live_in = people_live_in, distances=dist_dict)
    return render_template('info_city.html', city = location)
