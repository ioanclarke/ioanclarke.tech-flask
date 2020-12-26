from app import app
from flask import render_template
from app.scripts import OWScraper


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/projects/')
def projects():
    return render_template('projects.html', title='Projects')


@app.route('/stats')
def stats():
    scraper = OWScraper()
    role_names, role_SRs, hero_names, hero_times = scraper.get_stats()
    # role_names, role_SRs, hero_names, hero_times = (['Support', 'Damage', 'Tank'], [9999, 9999, 9999],
    # ['XXXXXXXX']*5, ['00:00:00']*5)
    print(role_names)
    return render_template('stats.html', title='Stats', role_names=role_names, role_srs=role_SRs, hero_names=hero_names,
                           hero_times=hero_times)

@app.route('/loading')
def loading():
    return render_template('loading.html', title='...')