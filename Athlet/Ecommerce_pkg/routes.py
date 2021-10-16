import secrets
from Ecommerce_pkg import app, db, bcrypt
from PIL import Image
from Ecommerce_pkg.forms import RegistrationForm, LoginForm ,UpdateAccountForm , addproductsForm
from flask import render_template ,url_for ,flash , redirect , request, session
from Ecommerce_pkg.models import Addproducts, Cart, User
from flask_login import login_user, current_user , logout_user , login_required
from werkzeug.utils import secure_filename
import os


@app.route("/")
def home():
    products = Addproducts.query.all()

    return render_template('index.html',products=products)

@app.route("/product")
def product():
    products = Addproducts.query.all()
    return render_template('product.html', products=products)

@app.route("/singleproduct/<int:product_id>")
def singleproduct(product_id):
    products = Addproducts.query.filter_by(id=product_id).all()
    for product in products:
        items = Addproducts.query.filter_by(category = product.category)
    return render_template('singleproduct.html', products=products, items=items)


@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}','succes')
        return redirect(url_for('login'))
    return render_template('register.html',title = 'Register', form = form)


@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            print(next_page)
            return redirect(next_page) if next_page else redirect(url_for('home')) 
    return render_template('login.html',title = 'Login', form = form)


@app.route('/index',methods=['GET','POST'])
def index():
    return render_template('index.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/uploads', picture_fn)

    op_size = (150, 150)
    img = Image.open(form_picture)
    img.thumbnail(op_size)
    img.save(picture_path)
    return picture_fn

@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('account details updated succesfully')
        return redirect(url_for('account'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # image_file = url_for('static',filename = 'images/featured/' + current_user)
    return render_template('account.html', form = form)

@app.route("/adminlogin",methods=['GET','POST'])
def adminlogin():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data =='nitin@gmail.com' and form.password.data == 'nitinsraju':
            flash('you have logged in succesfully')
            return redirect(url_for('home'))
        else:
            flash(' login unsuccesful') 
    return render_template('admin/login.html',title = 'Login', form = form  )

@app.route('/addproducts',methods=['GET','POST'])
def addproduct():
    form=addproductsForm()
    if form.validate_on_submit():
        product=Addproducts(name=form.name.data,description=form.description.data,price=form.price.data,category=form.category.data)
        if form.image.data:
            picture=save_picture(form.image.data)
            product.image=picture
        
        db.session.add(product)
        db.session.commit()
        flash('Item successfully added!', 'success')
        return redirect(url_for('addproduct'))
        # img_file=url_for('static',filename='book_pics/'+ book.image)
    return render_template('addproduct.html',form=form)

@app.route('/cart/',methods=['GET','POST'])
def cart():
    products = Cart.query.all()
    cart_len = len(products)
    return render_template('cart.html' , products = products, cart_len= cart_len)

@app.route('/cart/<int:product_id>',methods=['GET','POST'])
def add_to_cart(product_id):
    items = Addproducts.query.filter_by(id=product_id).all()
    for item in items:
        cartitem = Cart(id=product_id,name=item.name,price= item.price,image=item.image)
    db.session.add(cartitem)
    db.session.commit()
    flash('product added to cart')
    return redirect(url_for('cart'))

@app.route('/cart/clear_cart',methods=['GET','POST'])
def clear_cart():
    db.session.query(Cart).delete()
    db.session.commit()
    return redirect(url_for('cart'))