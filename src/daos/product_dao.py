"""
Product DAO (Data Access Object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import os
import db
from logger import Logger

class ProductDAO:
    def __init__(self):
        try:
            cluster, session = db.get_cassandra_connection()
            self.session = session
            self.cluster = cluster
            self.logger = Logger.get_instance("ProductDAO")
        except Exception as e:
            self.logger.debug("Erreur : " + str(e))

    def select_all(self):
        """ Select all products from Casandra """
        # TODO: cherchez les articles dans la base de données
        results = []
        return results

    def insert(self, product):
        """ Insert given product into Casandra """
        # TODO: ajoutez l'article dans la base de données
        self.logger.info(product)

    def close(self):
        self.session.shutdown()
        self.cluster.shutdown()