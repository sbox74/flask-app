from flask import Flask
from config import Config
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = 'login'

# must be here
from web_app import routes

if __name__ == '__main__':
    app.run()
