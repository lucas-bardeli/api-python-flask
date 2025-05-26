
# Importação
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

# Modelagem:
# Produto (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


# Rotas:
# Adicionar produto
@app.route('/api/products/add', methods=["POST"])
def add_product():
    data = request.json
    if (('name' in data) and ('price' in data)): 
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added successfully"})
    return jsonify({"message": "Invalid product data"}), 400


# Deletar produto
@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
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
    return jsonify({"message": "Product not found"}), 404


# Definir uma rota raiz (página inicial) e a função que será executada ao requisitar
@app.route('/hello')
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    app.run(debug=True)