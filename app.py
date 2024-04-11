import os
import json
from crud import create_job, update_job, get_jobs, add_favorite
from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
from flask_migrate import Migrate
from flask_login import login_required, current_user
from forms import searchForm
from model import connect_to_db, db, login_manager, Job, User, UserJob
from datetime import datetime
from dotenv import load_dotenv
import urllib.parse
from scraper.mntech import scrape_jobs

app = Flask(__name__, static_folder='static')

load_dotenv()
config_file_path = 'config.json'
if os.path.exists(config_file_path):
    with open(config_file_path, 'r') as f:
        config = json.load(f)
else:
    config = {}
app.config['SECRET_KEY'] = config['SECRET_KEY']
db_uri = config.get('DB_URI')

#blueprints
from users.views import users_blueprint
app.register_blueprint(users_blueprint, url_prefix='/users')

login_manager.init_app(app)
login_manager.login_view = 'users.login'
@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to access this page.', 'error')
    return redirect(url_for('users.login'))

connect_to_db(app, db_uri)
migrate = Migrate(app, db)

@app.route('/test', methods=['GET', 'POST'])
def test():
    return redirect(url_for('users.login'))

@app.route('/', methods=['GET', 'POST'])
async def home():

    form = searchForm()

    if form.validate_on_submit():
        encoded_search = form.search_term.data.replace(' ','+')
        encoded_location = urllib.parse.quote(form.search_location.data)

        print(f'encoded search {encoded_search}')

        results_found = await scrape_jobs(encoded_search, encoded_location, form.search_radius.data)

        for href, data in results_found.items():
            existing_job = Job.url_exists(href)
            if existing_job:
                existing_job_id = int(existing_job.id)
                print(existing_job_id)
                if existing_job.title != data['title'] or existing_job.company != data['company'] or existing_job.location != data['location'] or existing_job.description != data['description']:
                    update_job(existing_job_id, data)

                print(data.id)
            else:
                
                title = data['title']
                company = data['company']
                location = encoded_location
                description = data['description']
                url = data['url']
                search_term = encoded_search

                job = create_job(title, company, location, url, description, search_term)
                print('success')
                print(data)
                db.session.add(job)

            db.session.commit()
        return redirect(url_for('view_results', search_term=encoded_search))
    return render_template('home.html', form=form)

@app.errorhandler(404)
def error_404(e):
   return render_template("404.html")


@app.route('/results/<search_term>')
def view_jobs(search_term):

    results = get_jobs(search_term)
    results_json = []

    for result in results:
        results_json.append(result.json())

    return jsonify(results_json)




@app.route('/results', methods=['POST'])
def add_jobs():
    results = request.json.get('data')

    for result in results:
        search_result = create_job(result)
        db.session.add(search_result)

    db.session.commit()
    response = {'message': 'Received data successfully'}
    return jsonify(response), 200


@app.route('/results/update/<int:id>', methods=['PUT'])
def job_update(id):
        data = request.json
        update_job(id, data)
        db.session.commit()
        return jsonify({'message': 'Job updated successfully'}), 200


@app.route('/results/view_results/<search_term>')
def view_results(search_term):
    print(f"view results search term {search_term}")
    results = Job.query.filter_by(search_term=search_term).all()

    user_id = current_user.get_id()
    #csrf_token = generate_csrf()

    favorite_jobs = {}

    if user_id:
        user_jobs = UserJob.query.filter_by(user_id=user_id).all()
        for job in user_jobs:
            favorite_jobs[job.job_result_id] = job.favorite
    
    for result in results:
        result.favorite = favorite_jobs.get(result.id, False)

    return render_template('results.html', results=results, user_id=user_id)

@app.route('/toggle_favorite', methods=['GET', 'POST'])
@login_manager.unauthorized_handler
def toggle_favorite():
    print(current_user.is_authenticated)
    if not current_user.is_authenticated:
        print('i am not authenticated')
        flash('You must be authenticated to perform this action.', 'error')
        print('after flash')
        return redirect(url_for('users.login'))
    
    data = request.json
    user_id = current_user.get_id()
    job_id = data.get('result_id')
    print(user_id)

    if job_id is None:
        return jsonify({'message': 'Invalid request, user_id and job_id are required'}), 400

    user_job = UserJob.query.filter_by(user_id=user_id, job_result_id=job_id).first()

    if user_job:
        db.session.delete(user_job)
        db.session.commit()
        return jsonify({'message': 'Favorite removed successfully'}), 200
    else:
        user_job = UserJob(
            user_id=user_id,
            job_result_id=job_id,
            status='Interested',
            favorite=True,
            created_at=datetime.now(),
            last_modified=datetime.now()
        )
        db.session.add(user_job)
        db.session.commit()
        return jsonify({'message': 'Favorite added successfully'}), 200
    


if __name__=='__main__':
    app.run(debug=True)