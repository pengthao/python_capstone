from flask import Blueprint, render_template, redirect, request, url_for, flash , session, abort
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from model import User, Job, UserJob, db
from crud import update_favorite_job
from users.forms import LoginForm, RegistrationForm, searchForm, updateStatus

bcrypt = Bcrypt()

users_blueprint = Blueprint('users', __name__, template_folder='templates/users')

@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You logged out!')
    return redirect(url_for('home'))


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')

            next_url = request.args.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect(url_for('home'))

        else:
            flash('Invalid email or password. Please try again.', 'error')
    return render_template('login.html', form=form)
    
@users_blueprint.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        
        user = User(username = form.username.data,
                    email = form.email.data,
                    password = form.password.data)
        
        db.session.add(user)
        db.session.commit()
        print(user.json())
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', form=form)

@users_blueprint.route('/my_jobs', methods = ['GET', 'POST'])
def my_jobs():
    user_id = current_user.get_id()
    saved_jobs = UserJob.query.filter_by(user_id=user_id).all()
    job_results = []
    for job in saved_jobs:
        job_result = Job.query.filter_by(id=job.job_result_id).first()
        job_results.append((job_result))

    form = updateStatus()

    if request.method == 'POST':
        if form.validate_on_submit():
            print("Form validated successfully")
            job_id = request.form.get('job_id')
            update_favorite_job(user_id, job_id, form.status.data)
        else:
            print("Form validation failed. Errors:")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field '{field}': {error}")
    return render_template('my_jobs.html', form=form, job_results=job_results)
