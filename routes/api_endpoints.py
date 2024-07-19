from datetime import datetime, timedelta
import hashlib
from flask import Flask, Blueprint,redirect,url_for,render_template,request, jsonify
from dotenv import load_dotenv
import os
from os.path import join, dirname
from pymongo import MongoClient
import smtplib
import jwt
# MIMEMultipart send emails with both text content and attachments.
from email.mime.multipart import MIMEMultipart
# MIMEText for creating body of the email message.
from email.mime.text import MIMEText
# MIMEApplication attcing app-specific data (like csv files)
from email.mime.application import MIMEApplication

api_bp = Blueprint('api', __name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = os.environ.get('DB_NAME')
SENDER_PW = os.environ.get('SENDER_PW')
EMAIL1 = os.environ.get('EMAIL1')
EMAIL2 = os.environ.get('EMAIL2')
SECRET_KEY = os.environ.get('SECRET_KEY')

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

sender_email = EMAIL1
recipient_email = EMAIL2
sender_password = SENDER_PW
smtp_server = 'smtp.gmail.com'
smtp_port = 465

# endpoint for get message by contact
@api_bp.route('/contact', methods=['POST'])
def post_msg():
    person_sender = request.form['person_sender']
    user_message = request.form['message']
    
    message = MIMEMultipart()
    message['Subject'] = f'Message from {person_sender}!✨'
    message['From'] = sender_email
    message['To'] = recipient_email

    html = render_template('email_template.html', user_message=user_message, person_sender=person_sender)
    template = MIMEText(html, 'html', 'utf-8')
    message.attach(template)

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password) 
        server.sendmail(sender_email, recipient_email, message.as_string().encode('utf-8'))

    return jsonify({
        'msg': 'message sent succesfully!'
    })

# endpoint for login
@api_bp.route('/luji_portfolio/api/v1/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
    isUser = db.users.find_one({
        'username': username,
        'password': hashed_pw
    })

    if isUser:
        payload = {
            'id': username,
            'expired': (datetime.now() + timedelta(seconds= 60 * 60 * 24)).isoformat()
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'msg': 'login success!', 'token': token}), 200
    else:
        return jsonify({'result': 'failed', 'msg': 'login failed'})
    

#endpoint untuk project section
@api_bp.route('/luji_portfolio/api/v1/add_project', methods=['POST'])
def add_project():
    project_name = request.form['project_name']
    project_desc = request.form['project_description']
    project_link = request.form['project_link']
    project_thumbnail = request.files['project_thumbnail']
    curr_date = datetime.now().strftime('%d%m%Y-%H%M%S')

    # save the project thumbnail image to assets
    if project_thumbnail:
        img_path = os.path.join('static/assets/images/', f'project_img_{curr_date}.png')
        project_thumbnail.save(img_path)
    
    # save project data to db
    data = {
        'project_name': project_name,
        'project_desc': project_desc,
        'project_link': project_link,
        'project_thumbnail': img_path
    }

    db.projects.insert_one(data)
    return jsonify({'result': 'success', 'msg': 'New project added, sir!👌'}), 200

@api_bp.route('/luji_portfolio/api/v1/delete_project', methods=['POST'])
def delete_project():
    project_name = request.form['project_name']
    img_path = db.projects.find({'project_name': project_name}, {'project_thumbnail': 1, '_id': False})
    for path in img_path:
        if os.path.exists(path['project_thumbnail']):
            # delete the image from images folder
            os.remove(path['project_thumbnail'])
            db.projects.delete_one({'project_name': project_name})
            return jsonify({'result': 'success', 'msg': 'Project deleted, sir!👌'}), 200
        else:
            return jsonify({'result': 'failed', 'msg': 'project not found!'})

@api_bp.route('/luji_portfolio/api/v1/get_projects', methods=['GET'])
def get_projects():
    data = list(db.projects.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'data': data})