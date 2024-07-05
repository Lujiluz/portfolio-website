from datetime import datetime, timedelta
import hashlib
from flask import Flask, Blueprint,redirect,url_for,render_template,request, jsonify
from dotenv import load_dotenv
import os
from os.path import join, dirname
from pymongo import MongoClient


web_bp = Blueprint('web', __name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = os.environ.get('DB_NAME')
SECRET_KEY = os.environ.get('SECRET_KEY')

client = MongoClient(MONGO_URL)
db = client[DB_NAME]


@web_bp.route('/')
def home():
    return render_template('index.html')

@web_bp.route('/admin/login')
def admin_login():
    return render_template('admin_login.html')

@web_bp.route('/admin/dashboard')
def admin_dashboard():
    return render_template('pages/dashboard.html', page='dashboard')

@web_bp.route('/admin/projects')
def admin_projects():
    return render_template('/pages/projects.html', page='projects')

@web_bp.route('/admin/writings')
def admin_writings():
    return render_template('pages/writings.html', page='writings')
