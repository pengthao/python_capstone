import json
from flask import Blueprint, render_template, redirect, request, url_for, flash , session
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
import urllib.parse
from model import User, Job, db
from crud import create_job, update_job
from users.forms import LoginForm, RegistrationForm, searchForm
from scraper.mntech import scrape_jobs
from datetime import datetime



bcrypt = Bcrypt()

users_blueprint = Blueprint('users', __name__, template_folder='templates/users')

@users_blueprint.route('/welcome', methods=['GET', 'POST'])
@login_required
async def welcome_user():

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
    return render_template('welcome_user.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))



@users_blueprint.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):

            login_user(user)
            flash('Logged in Successfully!')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('users.welcome_user')

            return redirect(next)
        
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