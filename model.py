from flask_bcrypt import Bcrypt, generate_password_hash
from flask_restful import Resource, Api
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

@login_manager.user_loader
def get_by_username(username):
    user_data = User.get(username)
    return User.json(user_data) if user_data else None

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def __str__(self):
        return f"User Id: {self.id}"
    
    def check_password(self, password):
        print(f'check {password}')
        print(bcrypt.check_password_hash(self.password_hash, password))
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def json(self):
        return f"'id' : {self.id}, 'username' : {self.username}, 'email' : {self.email}, 'password' : {self.password_hash}"


class Job(db.Model):
    __tablename__ = "job_results"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    search_term = db.Column(db.String(255), nullable=False)
    
    def __init__(self, title, company, location, url, description, created_at, search_term):
        self.title = title
        self.company = company
        self.location = location
        self.url = url
        self.description = description
        self.created_at = created_at
        self.search_term = search_term

    def json(self):
        return f"'id' : {self.id}, 'title' : {self.title}, 'company' : {self.company}, 'location' : {self.location}, 'url' : {self.url}, 'description' : {self.description}, 'created_at' : {self.created_at}, 'search_term' : {self.search_term}"
    
    @classmethod
    def url_exists(cls, url):
        return cls.query.filter_by(url=url).first() is not None

class UserJob(db.Model):
    __tablename__ = "user_jobs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_result_id = db.Column(db.Integer, db.ForeignKey('job_results.id'), nullable=False)
    status = db.Column(db.Enum('Interested', 'Applied', 'Accepted', 'Not Interested', name='status'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    last_modified = db.Column(db.DateTime)
    favorite = db.Column(db.Boolean)

    user = db.relationship('User', backref=db.backref('user_jobs', lazy=True))
    job_result = db.relationship('Job', backref=db.backref('user_jobs', lazy=True))


class UserTrackedSearch(db.Model):
    __tablename__ = "user_tracked_searches"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    search = db.Column(db.Integer, nullable=False)  # Assuming this is the search term or identifier
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('user_tracked_searches', lazy=True))


class JobResultTracked(db.Model):
    __tablename__ = "job_results_tracked"

    id = db.Column(db.Integer, primary_key=True)
    job_result_id = db.Column(db.Integer, db.ForeignKey('job_results.id'), nullable=False)
    tracked_search_id = db.Column(db.Integer, db.ForeignKey('user_tracked_searches.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    job_result = db.relationship('Job', backref=db.backref('job_results_tracked', lazy=True))
    tracked_search = db.relationship('UserTrackedSearch', backref=db.backref('job_results_tracked', lazy=True))



def connect_to_db(flask_app, db_uri=None, echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(flask_app)

    print("Connected to the db!")
