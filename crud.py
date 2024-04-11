from model import db, User, Job, UserJob, connect_to_db
from datetime import datetime
from flask import request, jsonify


def create_job(title, company, location, url, description, search_term):
    
    job = Job(
            title=title,
            company=company,
            location=location,
            url=url,
            description=description,
            created_at=datetime.now(),
            search_term=search_term
        )
    
    print('im adding you in')
    return job

def update_job(id, data):
    data = request.json
    existing_job = Job.query.get_or_404(id)

    existing_job.title = data['title']
    existing_job.company = data['company']
    existing_job.location = data['location']
    existing_job.description = data['description']

def get_jobs(search_term):
    similar_jobs = Job.query.filter(Job.search_term.ilike(f"%{search_term}%")).all()
    return similar_jobs


def add_favorite(user_id, job_id):
    user_job = UserJob(
        user_id = user_id,
        job_result_id = job_id,
        status = 'Interested',
        created_at = datetime.now(),
        last_modified = datetime.now()
    )
    print('Adding to favorites')
    return user_job

def update_favorite_job(user_id, job_id, status):
    job = UserJob.query.filter_by(user_id=user_id, job_result_id=job_id).first()
    
    if job:
        job.status = status
        job.last_modified = datetime.now()
        db.session.commit()
        return jsonify({'message': 'Favorite updated successfully'}), 200
    else:
        return jsonify({'error': 'Job not found'}), 404



if __name__ == '__main__':
    from app import app
    connect_to_db(app)