from Ecommerce_pkg import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable= False)
    email = db.Column(db.String(100),unique=True,nullable= False)
    password = db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"User('{ self.username }','{ self.email }')" 

class Product(db.Model, UserMixin):
    product_id = db.Column(db.Integer,primary_key=True)
    productname = db.Column(db.String(20),unique=True,nullable= False)
    description = db.Column(db.String(100),unique=True,nullable= False)
    price = db.Column(db.String(5),nullable=False)
    img_link = db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"User('{ self.productname }')" 


class Addproducts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(5),nullable=False)
    category = db.Column(db.String(20),nullable=False)

    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    cartitem = db.relationship('Cart',backref=db.backref('product', lazy=True))
    
    image = db.Column(db.String(50),nullable=False)
    def __repr__(self):
        return f"Addproducts('{ self.name }')" 


# class Category(db.Model,UserMixin):
#     id = db.Column(db.Integer,primary_key=True)
#     name = db.Column(db.String(30),unique=True,nullable= False)

#     def __repr__(self):
#         return f"User('{ self.name }')" 
class Cart(db.Model):
    item_id = db.Column(db.Integer,primary_key=True)
    id = db.Column(db.Integer,db.ForeignKey('addproducts.id'),nullable=False)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.String(5),nullable=False)
    image = db.Column(db.String(50),nullable=False)



