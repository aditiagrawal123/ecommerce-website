
from flask import Flask,render_template,request, flash, redirect, session, url_for, send_file
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from base64 import b64encode
import base64
import os
from shop import app,db,bcrypt
from .forms import RegistrationForm,LoginForm
from .models import Admin,Brand,Category


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash('Please login first','danger')
        return redirect(url_for('login'))
    return render_template('admin/index.html',title="admin")





@app.route('/registration', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password=bcrypt.generate_password_hash(form.password.data)
        user = Admin(name=form.name.data,username=form.username.data, email=form.email.data,
                     password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering','success')
        return redirect(url_for('login'))
    return render_template('admin/registration.html', form=form,title="Registration form")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user=Admin.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            session['email']=form.email.data
            flash(f'Welcome {user.name} You are logged in','success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash(f'Wrong Password please try again','danger')
    return render_template('admin/login.html', form=form,title="Login form")


# def brands():
#     brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
#     return brands

# def categories():
#     categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
#     return 


@app.route('/addbrand',methods=['GET','POST'])
def addbrand():
    if request.method =="POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('admin/addbrand_cat.html', title='Add brand',brands='brands')


@app.route('/addcategory',methods=['GET','POST'])
def addcategory():
    if request.method =="POST":
        getcategory = request.form.get('category')
        category = Category(name=getcategory)
        db.session.add(category)
        flash(f'The category {getcategory} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addcategory'))
    return render_template('admin/addbrand_cat.html', title='Add category')