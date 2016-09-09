import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import basedir
from flask.ext.mail import Message, Mail
 
mail = Mail()

app = Flask(__name__)
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir,'tmp'))
db = SQLAlchemy(app)

from mycircle import views, models

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'pundir.pd@gmail.com'
app.config["MAIL_PASSWORD"] = ''
 
mail.init_app(app)
