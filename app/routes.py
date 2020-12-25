from app import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/projects')
def projects():
    return render_template('projects.html', title='Projects')


@app.route('/stats')
def stats():
    return render_template('stats.html', title='Stats')
