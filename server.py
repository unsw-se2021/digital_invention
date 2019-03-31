from flask import Flask
from flask_login import LoginManager
from RaisinSystem import RaisinSystem

app = Flask(__name__)
ERROR_STATEMENT = "Big fat error"

app.config['SECRET_KEY'] = 'Another_highly_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
system = RaisinSystem()