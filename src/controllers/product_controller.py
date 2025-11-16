"""
Product controller
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import uuid
from flask import jsonify
from daos.product_dao import ProductDAO
from logger import Logger
from models.product import Product

class ProductController:
    def __init__(self):
        self.dao = ProductDAO()
        self.logger = Logger.get_instance("Controller")

    def list_products(self):
        """ List all products """
        # TODO
        pass
        
    def create_product(self, request):
        """ Create a new product based on user inputs """
        # TODO
        self.logger.debug(request.get_json())
        pass
            
