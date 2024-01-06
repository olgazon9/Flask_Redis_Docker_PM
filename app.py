from flask import Flask, render_template, request, jsonify
import redis
import json

app = Flask(__name__)
db = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

@app.route('/product', methods=['POST'])
def create_product():
    product_data = request.json
    product_id = product_data['id']
    db.set(product_id, json.dumps(product_data))  # Store as JSON string
    return jsonify(product_data), 201

@app.route('/fetch-products', methods=['GET'])
def fetch_products():
    product_keys = db.keys()  # Get all product keys
    products = []
    for key in product_keys:
        product_data = db.get(key)
        try:
            product = json.loads(product_data)
            products.append(product)
        except json.JSONDecodeError:
            print(f"Invalid JSON data for key {key}: {product_data}")
    return jsonify(products)

@app.route('/product/<product_id>', methods=['PUT'])
def update_product(product_id):
    product_data = request.json
    if db.exists(product_id):
        db.set(product_id, json.dumps(product_data))
        return jsonify(product_data), 200
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route('/product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    if db.exists(product_id):
        db.delete(product_id)
        return jsonify({"success": "Product deleted"}), 200
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
