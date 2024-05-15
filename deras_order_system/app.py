from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default=0)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship('Product')

with app.app_context():
    db.create_all()

@app.route('/')
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
def admin():
    products = Product.query.all()
    return render_template('admin.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    product_name = request.form.get('product_name')
    new_product = Product(name=product_name, quantity=0)
    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
