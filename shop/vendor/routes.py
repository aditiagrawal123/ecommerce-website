import re
from flask import Flask,render_template,request, flash, redirect, session, url_for, send_file
from datetime import datetime
from flask_login import current_user,login_required,login_user
from flask_sqlalchemy import SQLAlchemy
from base64 import b64encode
import base64
import os

from sqlalchemy import null
from shop import app,db,bcrypt,login_manager
from .models import product,Vendor
from .forms import RegistrationForm,LoginForm
from shop.admin.models import Brand,Category

@app.route('/vendor')
def vendor():
    if 'email' not in session:
        flash('Please login first','danger')
        return redirect(url_for('vendor_login'))
    
    return render_template('vendor/index.html',title="sell_here")

@app.route('/vendor_registration', methods=['GET', 'POST'])
def vendor_register():
    
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password=bcrypt.generate_password_hash(form.password.data)
        vendor = Vendor(name=form.name.data,username=form.username.data, email=form.email.data,
                     password=hash_password)
                   
        db.session.add(vendor)
        db.session.commit()
        flash(f'Thanks for registering','success')
        return redirect(url_for('vendor_login'))
    return render_template('admin/registration.html', form=form,title="Registration form")


@app.route('/vendor_login', methods=['GET', 'POST'])
def vendor_login():
    
    form=LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        vendor=Vendor.query.filter_by(email=form.email.data).first()
        if vendor and bcrypt.check_password_hash(vendor.password,form.password.data):
            login_user(vendor)
            session['email']=form.email.data
            flash(f'Welcome {vendor.name} You are logged in','success')
            
            return redirect(request.args.get('next') or url_for('vendor'))
        else:
            flash(f'Wrong Password please try again','danger')
    return render_template('admin/login.html', form=form,title="Login form")

def render_picture(data):

    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic


@app.route('/vendorproducts',methods=['GET','POST'])
@login_required
def products():
    if current_user.is_authenticated:

     brands=Brand.query.all()
     categories=Category.query.all()
     print(current_user)
     vendor_id=current_user.id
     if request.method=='POST':
         
         name=request.form['product-name']
         file=request.files['fileToUpload']
         data=file.read()
         render_file = render_picture(data)
         price=request.form['price']
         desc=request.form['product-description']
         vendor_id=current_user.id
         brand=request.form['brand']
         category=request.form['category']
         print(vendor_id)
 
         newFile = product(name=name,data=data,rendered_data=render_file,price=price,desc=desc,vendor_id=vendor_id,brand=brand,category=category)
         db.session.add(newFile)
         db.session.commit()
         #print(brand)
     
     table=product.query.all()
     
     
     return render_template('vendor/vendor_products.html',methods=['GET','POST'],table=table,brand=brands,category=categories,vendor_id=vendor_id)
    
@app.route('/update/<int:id>',methods=['GET','POST'])
#@login_required
def update(id):
     brands=Brand.query.all()
     categories=Category.query.all()
     if request.method=='POST':
         
         name=request.form['product-name']
         file=request.files['fileToUpload']
         data=file.read()
         render_file = render_picture(data)
         price=request.form['price']
         desc=request.form['product-description']
         brand=request.form['brand']
         category=request.form['category']
         to_upd=product.query.filter_by(id=id).first()
         
         to_upd.name=name
         to_upd.file=file
         to_upd.data=data
         to_upd.render_file=render_file
         to_upd.price=price
         to_upd.desc=desc
         to_upd.brand=brand
         to_upd.category=category
         db.session.add(to_upd)
         db.session.commit()
         return redirect("/vendorproducts")
     to_upd=product.query.filter_by(id=id).first()
     return render_template('vendor/update.html',to_upd=to_upd,brand=brands,category=categories)

@app.route('/delete/<int:id>')
#@login_required
def delete(id):
     to_del=product.query.filter_by(id=id).first()
     db.session.delete(to_del)
     db.session.commit()
     return redirect("/vendorproducts")