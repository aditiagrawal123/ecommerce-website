


from flask import Flask,render_template,request, flash, redirect, url_for, send_file
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from base64 import b64encode
import base64
from io import BytesIO
import os
from admin.forms import RegistrationForm
from flask_bcrypt import Bcrypt

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False



@app.route('/')
def home_page():
    return render_template('customer/customer_home.html')


@app.route('/signup')
def signup():
    return render_template('customer/customer_signup.html',title="Registration")





db=SQLAlchemy(app)
class product(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, nullable=False)
    data = db.Column(db.LargeBinary)
    rendered_data = db.Column(db.Text)
    price=db.Column(db.Integer)
    desc=db.Column(db.String)
    brand=db.Column(db.String, nullable=False)
    category=db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} - {self.name}"
@app.route('/sellhere')
def sell():
    return render_template('sell_signup.html')

def render_picture(data):

    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic


@app.route('/sellhere_products',methods=['GET','POST'])
def products():
    if request.method=='POST':
        id=request.form['product-id']
        name=request.form['product-name']
        file=request.files['fileToUpload']
        data=file.read()
        render_file = render_picture(data)
        price=request.form['price']
        desc=request.form['product-description']
        brand=request.form['brand']
        category=request.form['category']
        newFile = product(id=id,name=name,data=data,rendered_data=render_file,price=price,desc=desc,brand=brand,category=category)
        db.session.add(newFile)
        db.session.commit()
    table=product.query.all()
    return render_template('vendor/vendor_products.html',methods=['GET','POST'],table=table)
    
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    if request.method=='POST':
        id=request.form['product-id']
        name=request.form['product-name']
        file=request.files['fileToUpload']
        data=file.read()
        render_file = render_picture(data)
        price=request.form['price']
        desc=request.form['product-description']
        brand=request.form['brand']
        category=request.form['category']
        to_upd=product.query.filter_by(id=id).first()
        to_upd.id=id
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
        return redirect("/sellhere_products")
    to_upd=product.query.filter_by(id=id).first()
    return render_template('vendor/update.html',to_upd=to_upd)

@app.route('/delete/<int:id>')
def delete(id):
    to_del=product.query.filter_by(id=id).first()
    db.session.delete(to_del)
    db.session.commit()
    return redirect("/sellhere_products")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/registration', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                      form.password.data)
        db.session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('admin/registration.html', form=form,title="Signup form")


   



if __name__=="__main__":
    app.run(debug=True)
