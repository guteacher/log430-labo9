
"""
API tutorial: Flask + Apache Cassandra
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs: Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import uuid
import db
import config
from flask import Flask, jsonify, request
from controllers.product_controller import ProductController

db.setup_database()
app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# TODO: ajoutez les endpoints

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)