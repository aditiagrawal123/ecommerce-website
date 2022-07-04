from turtle import title
from flask import Flask,render_template,request, flash, redirect, session, url_for, send_file
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from base64 import b64encode
import base64
import os
from shop import app,db,bcrypt
from shop.vendor.models import product

@app.route('/')
def home_page():
    products=product.query.all()
    return render_template('customer/customer_home.html',title="MYKAA!",products=products)


@app.route('/signup')
def signup():
    return render_template('customer/customer_signup.html',title="signup")
