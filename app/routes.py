from app import app
from flask import render_template
from app.scripts import OWScraper, SmiteScraper


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/projects/')
def projects():
    return render_template('projects.html', title='Projects')


@app.route('/stats')
def stats():
    if app.debug:
        ow_role_names, ow_role_srs  = ['Support', 'Damage', 'Tank'], [9999, 9999, 9999]
        ow_hero_names, ow_hero_times = ['X'*8] * 5, ['00:00:00'] * 5
        ow_update_time = '00:00:00 GMT  00-00-0000'
        smite_level, smite_playtime,  = [999, '9999h']
        smite_matches_played, smite_win_loss, smite_kda,  = 9999, '99.99%', 9.99
        smite_update_time = '00:00:00 GMT  00-00-0000'
    else:
        ow_scraper = OWScraper()
        smite_scraper = SmiteScraper()
        ow_role_names, ow_role_srs, ow_hero_names, ow_hero_times, ow_update_time = ow_scraper.get_stats()
        smite_level, smite_playtime, smite_matches_played, smite_win_loss, smite_kda, smite_update_time = smite_scraper.get_stats()
        print(ow_update_time, smite_update_time)

    return render_template('stats.html', title='Stats', ow_role_names=ow_role_names, ow_role_srs=ow_role_srs,
                           ow_hero_names=ow_hero_names, ow_hero_times=ow_hero_times, ow_update_time=ow_update_time,
                           smite_level=smite_level,
                           smite_playtime=smite_playtime, smite_matches_played=smite_matches_played,
                           smite_win_loss=smite_win_loss, smite_kda=smite_kda, smite_update_time=smite_update_time)


@app.route('/loading')
def loading():
    return render_template('loading.html', title='...')
