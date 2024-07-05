from flask import Flask
from routes.page_routes import web_bp
from routes.api_endpoints import api_bp


app = Flask(__name__)
app.register_blueprint(web_bp)
app.register_blueprint(api_bp)


if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)