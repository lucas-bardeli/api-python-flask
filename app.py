
# Importação
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

# Modelagem:
# Usuário (id, username, password, cart)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    cart = db.relationship('CartItem', backref='user.id', lazy=True)

# Produto (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

# Carrinho (id, user_id, product_id)
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

# Autenticação
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rotas:
# Login
@app.route('/login', methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get("username")).first()
    if (user and (data.get("password") == user.password)):
        login_user(user)
        return jsonify({"message": "Logged in successfully"})
    return jsonify({"message": "Unauthorized. Invalid credentials"}), 401

# Logout
@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})


# Users:
# Recuperar usuários
@app.route('/api/users', methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "username": user.username,
            "password": user.password
        })
    return jsonify(user_list)

# Recuperar usuário pelo id
@app.route('/api/users/<int:user_id>', methods=["GET"])
def get_user_details(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "id": user.id,
            "name": user.username,
            "password": user.password
        })
    return jsonify({"message": "Not Found. User not available"}), 404

# Procurar um usuário pela query
@app.route('/api/users/search', methods=["GET"])
def search_users():
    query = request.args.get('q')
    if not query:
        return jsonify({"message": "Query parameter 'q' is required"}), 400
    users = User.query.filter(User.username.ilike(f'%{query}%')).all()
    if not users:
        return jsonify({"message": "Not Found. No users found for the search query"}), 404
    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "username": user.username,
            "password": user.password
        })
    return jsonify(user_list)

# Adicionar usuário
@app.route('/api/users/add', methods=["POST"])
@login_required
def add_user():
    data = request.json
    if (("username" in data) and ("password" in data)): 
        user = User(username=data["username"], password=data["password"])
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User added successfully"})
    return jsonify({"message": "Invalid user data"}), 400

# Atualizar usuário
@app.route('/api/users/update/<int:user_id>', methods=["PUT"])
@login_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Not Found. User not available"}), 404
    data = request.json
    if ("username" in data):
        user.username = data["username"]
    if ("password" in data):
        user.password = data["password"]
    db.session.commit()
    return jsonify({"message": "User updated successfully"})

# Deletar usuário
@app.route('/api/users/delete/<int:user_id>', methods=["DELETE"])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"message": "Not Found. User not available"}), 404


# Produtos:
# Recuperar produtos
@app.route('/api/products', methods=["GET"])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_list.append({
            "id": product.id,
            "name": product.name,
            "price": product.price
        })
    return jsonify(product_list)

# Recuperar produto pelo ID
@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify({"message": "Not Found. Product not available"}), 404

# Procurar um produto pela query
@app.route('/api/products/search', methods=["GET"])
def search_products():
    query = request.args.get('q')
    if not query:
        return jsonify({"message": "Query parameter 'q' is required"}), 400
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    if not products:
        return jsonify({"message": "Not Found. No products found for the search query"}), 404
    product_list = []
    for product in products:
        product_list.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify(product_list)

# Adicionar produto
@app.route('/api/products/add', methods=["POST"])
@login_required
def add_product():
    data = request.json
    if (("name" in data) and ("price" in data)): 
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added successfully"})
    return jsonify({"message": "Invalid product data"}), 400

# Atualizar produto
@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Not Found. Product not available"}), 404
    data = request.json
    if ("name" in data):
        product.name = data["name"]
    if ("price" in data):
        product.price = data["price"]
    if ("description" in data):
        product.description = data["description"]
    db.session.commit()
    return jsonify({"message": "Product updated successfully"})

# Deletar produto
@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
def delete_product(product_id):
    # Recuperar o produto da base de dados
    product = Product.query.get(product_id)
    # Verificar se o produto existe
    if product:
        # Se existe, apagar da base de dados
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})
    # Se não existe, retornar 404 not found
    return jsonify({"message": "Not Found. Product not available"}), 404


# Carrinho:
# Adicionar produtos ao carrinho
@app.route('/api/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    user = User.query.get(int(current_user.id))
    product = Product.query.get(product_id)
    if (user and product):
        cart_item = CartItem(user_id=user.id, product_id=product.id)
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item added to the cart successfully'})
    return jsonify({'message': 'Failed to add item to the cart'}), 400

# Remover itens do carrinho
@app.route('/api/cart/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_cart(product_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item removed from the cart successfully'})
    return jsonify({'message': 'Failed to remove item from the cart'}), 400

# Listagem do carrinho
@app.route('/api/cart', methods=['GET'])
@login_required
def view_cart():
    user = User.query.get(int(current_user.id))
    cart_items = user.cart
    cart_content = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        cart_content.append({
            "id": item.id,
            "user_id": item.user_id,
            "product_id": item.product_id,
            "product_name": product.name,
            "product_price": product.price
        })
    return jsonify(cart_content)

# Fechar carrinho
@app.route('/api/cart/checkout', methods=['POST'])
@login_required
def checkout():
    user = User.query.get(int(current_user.id))
    cart_items = user.cart
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Checkout successful. Cart has been cleared'})


# Definir uma rota raiz (página inicial) e a função que será executada ao requisitar
@app.route('/')
def hello_world():
    return "<h1>Hello, World!</h1>"

if __name__ == "__main__":
    app.run(debug=True)
    