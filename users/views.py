from flask import Blueprint, render_template, redirect, request, url_for, flash , session, abort
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from users.forms import LoginForm, RegistrationForm, updateStatus
from model import User, Job, UserJob, db
from crud import update_favorite_job

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
    

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user_check = User.query.filter_by(email=form.email.data).first()

        if not user_check:
            user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data)

            db.session.add(user)
            db.session.commit()
            flash('Thanks for registration!')
            return redirect(url_for('users.login'))
        else:
            flash('This email has already been taken')

    return render_template('register.html', form=form)


@users_blueprint.route('/my_jobs', methods = ['GET', 'POST'])
def my_jobs():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    user_id = current_user.get_id()
    saved_jobs = UserJob.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)
    job_results = []

    sort_option = request.args.get('sort')
    if sort_option == 'recent':
        saved_jobs_query = UserJob.query.filter_by(user_id=user_id).order_by(UserJob.last_modified.desc())
    elif sort_option == 'status':
        saved_jobs_query = UserJob.query.filter_by(user_id=user_id).order_by(UserJob.status)

    for job in saved_jobs:
        job_result = Job.query.filter_by(id=job.job_result_id).first()
        job_results.append((job_result))

    form = updateStatus()

    if request.method == 'POST':
        if form.validate_on_submit():
            job_id = request.form.get('job_id')
            update_favorite_job(user_id, job_id, form.status.data)

            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field '{field}': {error}")
    return render_template('my_jobs.html', form=form, job_results=job_results, saved_jobs=saved_jobs, sort_option=sort_option)
