import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = os.environ.get('DB_NAME')

client = MongoClient(MONGO_URL)
db = client[DB_NAME]


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# endpoint for get message by contact
@app.route('/contact', methods=['POST'])
def post_msg():
    email = request.form['email']
    message = request.form['message']
    data = {
        'email': email,
        'message': message
    }
    
    db.message.insert_one(data)
    return jsonify({
        'msg': 'message sent succesfully!'
    })
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=3000, debug=True)