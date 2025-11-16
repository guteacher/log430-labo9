"""
Product model
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

class Product:
    def __init__(self, product_id, name, sku, price):
        self.id = product_id
        self.name = name
        self.sku = sku
        self.price = price