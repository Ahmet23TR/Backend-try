from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Product, User
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@main.route('/products', methods=['GET'])
@login_required
def get_products():
    products = Product.query.all()
    return jsonify([{"id": product.id, "name": product.name, "quantity": product.quantity} for product in products])

@main.route('/products', methods=['POST'])
@login_required
def add_product():
    name = request.form.get('name')
    
    if name:
        new_product = Product(name=name)
        db.session.add(new_product)
        db.session.commit()
        flash('Ürün başarıyla eklendi!', 'success')
    else:
        flash('Ürün eklenirken bir hata oluştu. Lütfen ürün adını girin.', 'danger')
    
    return redirect(url_for('main.index'))

@main.route('/add_order', methods=['POST'])
@login_required
def add_order():
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', type=int)
    
    product = Product.query.get(product_id)
    if product:
        product.quantity += quantity
        db.session.commit()
        flash('Sipariş başarıyla eklendi!', 'success')
    else:
        flash('Ürün bulunamadı!', 'danger')
    
    return redirect(url_for('main.index'))

@main.route('/products/<int:id>', methods=['PUT'])
@login_required
def update_product(id):
    data = request.json
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    product.name = data['name']
    product.quantity = data['quantity']
    db.session.commit()
    return jsonify({"id": product.id, "name": product.name, "quantity": product.quantity})

@main.route('/delete_product', methods=['POST'])
@login_required
def delete_product():
    product_id = request.form.get('product_id', type=int)
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        flash('Ürün başarıyla silindi!', 'success')
    else:
        flash('Ürün bulunamadı!', 'danger')
    
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        
        flash('Login failed. Check your username and/or password.', 'danger')
    
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))
