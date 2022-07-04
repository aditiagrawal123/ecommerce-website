from shop import db ,login_manager
from flask_login import UserMixin,current_user
from shop.admin.models import Brand,Category

@login_manager.user_loader
def user_loader(user_id):     
     return Vendor.query.get(user_id)


class Vendor(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    db.relationship('product', backref='vendor', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username
class product(db.Model):
     id=db.Column(db.Integer, primary_key=True)
     name=db.Column(db.String, nullable=False)
     data = db.Column(db.LargeBinary)
     rendered_data = db.Column(db.Text)
     price=db.Column(db.Integer)
     desc=db.Column(db.String)
     vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'),
        nullable=False)
    #  brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    #  brand = db.relationship('Brand',backref=db.backref('brands', lazy=True))
     
     
     brand=db.Column(db.String, nullable=False)
     category=db.Column(db.String, nullable=False)
     
     
     
     def __repr__(self) -> str:
         return f"{self.id} - {self.name}"


db.create_all()