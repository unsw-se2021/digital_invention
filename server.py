from flask import Flask
from flask_login import LoginManager
from RaisinSystem import RaisinSystem
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)
ERROR_STATEMENT = "Big fat error"

app.secret_key = '123abc'

login_manager = LoginManager()
login_manager.init_app(app)
system = RaisinSystem()