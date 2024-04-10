import os
import json
from crud import create_job, update_job, get_jobs, add_favorite
from flask import Flask, Blueprint, render_template, jsonify, request, session, redirect, url_for
from flask_migrate import Migrate
from flask_wtf.csrf import generate_csrf
from flask_login import login_required, current_user
from forms import favorite, searchForm
from model import connect_to_db, db, login_manager, Job, User, UserJob
from datetime import datetime
from dotenv import load_dotenv

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

login_manager.init_app(app)
login_manager.login_view = 'user.login'

connect_to_db(app, db_uri)
migrate = Migrate(app, db)

#blueprints
from users.views import users_blueprint
app.register_blueprint(users_blueprint, url_prefix='/users')


@app.route('/')
def home():
    return render_template('home.html')

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
@login_required
def toggle_favorite():
    data = request.json
    user_id = current_user.get_id()
    job_id = data.get('result_id')
    

    print(f"user_id {user_id}")
    print(f"job_id {job_id}")


    if user_id is None or job_id is None:
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