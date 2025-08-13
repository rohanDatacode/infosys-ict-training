from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash

from config import Config
from models import db, User, Product, Cart
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 🔧 Create tables and default products
def create_tables():
    with app.app_context():
        db.create_all()
        if Product.query.count() == 0:
            db.session.add_all([
                Product(name="T-shirt", price=500, description="Cotton T-shirt"),
                Product(name="Shoes", price=1200, description="Running shoes"),
                Product(name="Watch", price=1500, description="Smartwatch")
            ])
            db.session.commit()

# 🏠 Home
@app.route('/')
def home():
    return render_template('home.html')

# 📝 Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# 🔐 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('products'))
        else:
            error = "Invalid email or password"
    return render_template('login.html', form=form, error=error)

# 🚪 Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# 🛍️ View Products
@app.route('/products')
@login_required
def products():
    items = Product.query.all()
    return render_template('product_list.html', products=items)

# ➕ Add to Cart
@app.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('cart'))

# 🛒 View Cart
@app.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    return render_template('cart.html', cart=cart_items)

# 💳 Checkout
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        total = sum(item.product.price * item.quantity for item in cart_items)

        # Clear the cart
        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()

        flash('Purchase successful!', 'success')
        return render_template('thankyou.html', name=name, total=total)

    return render_template('billing.html', cart=cart_items)

# 🚀 Run App
if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
