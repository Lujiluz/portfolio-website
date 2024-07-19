from datetime import datetime, timedelta
import hashlib
from flask import Flask, Blueprint, flash, redirect, url_for, render_template, request, jsonify
from dotenv import load_dotenv
import os
from os.path import join, dirname
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import login_manager

web_bp = Blueprint('web', __name__)

dotenv_path = join(dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = os.environ.get('DB_NAME')

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

class User(UserMixin):
    def __init__(self, username):
        self.username = username
        
    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)

@login_manager.user_loader
def load_user(username):
    user = db.users.find_one({'username': username})
    if not user:
        return None
    return User(username=user['username'])

@web_bp.route('/')
def home():
    return render_template('index.html')

@web_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return jsonify(success=True, redirect=url_for('web.admin_dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.users.find_one({'username': username})

        if user and User.check_password(user['password'], password):
            user_obj = User(username=user['username'])
            login_user(user_obj)
            return jsonify(success=True, redirect=url_for('web.admin_dashboard'))
        else:
            return jsonify(success=False, message='Invalid username or password')

    return render_template('admin_login.html')

@web_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template('pages/dashboard.html', page='dashboard')

@web_bp.route('/admin/projects')
@login_required
def admin_projects():
    return render_template('pages/projects.html', page='projects')

@web_bp.route('/admin/writings')
@login_required
def admin_writings():
    return render_template('pages/writings.html', page='writings')

@web_bp.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return jsonify(success=True, redirect=url_for('web.admin_login'))
