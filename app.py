from flask import Flask
from routes.page_routes import web_bp
from routes.api_endpoints import api_bp
from extensions import login_manager
from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get('SECRET_KEY')


app = Flask(__name__)
app.secret_key = SECRET_KEY

login_manager.init_app(app)

app.register_blueprint(web_bp)
app.register_blueprint(api_bp)


if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)