from datetime import datetime, timedelta
import hashlib
from flask import Flask, Blueprint,redirect,url_for,render_template,request, jsonify
from dotenv import load_dotenv
import os
from os.path import join, dirname
from pymongo import MongoClient
import smtplib
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
