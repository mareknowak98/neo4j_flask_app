from flask import Flask, request, session, redirect, url_for, render_template, flash
from .models import Person
import os


def create_app():
    app = Flask(__name__)
    return app

app=create_app()
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET','POST'])
def index():
    # p = list_all_persons()
    # l = list_all_locations()
    return render_template('index.html')


@app.route('/person/add', methods=['GET','POST'])
def add_person():
    if request.method == 'POST':
        name = request.form['name']
        if not Person(name).add():
            flash('Osoba z tym imieniem istnieje w bazie!')
        else:
            return redirect(url_for('index'))
    return render_template('add_person.html')