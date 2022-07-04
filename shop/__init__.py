from flask import Flask,render_template,request, flash, redirect, url_for, send_file
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from base64 import b64encode
import base64
import os
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='DJDNBFJEJJ262544'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

from shop.admin import routes
from shop.vendor import routes
from shop.customer import routes