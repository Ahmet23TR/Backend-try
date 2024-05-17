from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Güvenliğiniz için değiştirin
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user')  # 'admin' veya 'user'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default=0)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship('Product', backref='orders')

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def home():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/api/orders', methods=['POST'])
def add_order():
    data = request.json
    product_name = data['product_name']
    quantity = data['quantity']
    product = Product.query.filter_by(name=product_name).first()
    if product:
        product.quantity += int(quantity)
        new_order = Order(product_id=product.id, quantity=quantity)
        db.session.add(new_order)
        db.session.commit()
        return jsonify({"message": "Order added successfully!"}), 201
    return jsonify({"message": "Product not found"}), 404

@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        return redirect(url_for('home'))
    products = Product.query.all()
    return render_template('admin.html', products=products)

@app.route('/add_product', methods=['POST'])
@login_required
def add_product():
    if current_user.role != 'admin':
        return redirect(url_for('home'))
    product_name = request.form.get('product_name')
    new_product = Product(name=product_name, quantity=0)
    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete_product', methods=['POST'])
@login_required
def delete_product():
    if current_user.role != 'admin':
        return redirect(url_for('home'))
    product_id = request.form.get('product_id')
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/update_product', methods=['POST'])
@login_required
def update_product():
    if current_user.role != 'admin':
        return redirect(url_for('home'))
    product_id = request.form.get('product_id')
    new_name = request.form.get('product_name')
    product = Product.query.get(product_id)
    if product:
        product.name = new_name
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('register'))
        new_user = User(username=username, password=password, role='user')
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('home'))
        flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)