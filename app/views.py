from flask import Flask, request, session, redirect, url_for, render_template, flash

def create_app():
    app = Flask(__name__)
    return app

app=create_app()

@app.route('/', methods=['GET','POST'])
def index():
    # p = list_all_persons()
    # l = list_all_locations()
    return render_template('index.html')