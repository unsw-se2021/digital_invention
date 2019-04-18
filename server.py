from flask import Flask
from flask_login import LoginManager
from RaisinSystem import RaisinSystem
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

app.secret_key = 'Fordsjh Gjfhdfdjfhd Ujhdfr B02'

login_manager = LoginManager()
login_manager.init_app(app)
system = RaisinSystem()