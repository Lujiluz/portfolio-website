# extensions.py
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'web.admin_login'
