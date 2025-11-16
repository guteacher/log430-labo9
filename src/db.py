"""
Database connections
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs: Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import config
from logger import Logger
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

logger = Logger.get_instance("DB")

def get_cassandra_connection():
    """Connect to Cassandra"""
    # TODO: ajoutez le code
    pass


def setup_database():
    """Setup keystores and tables"""
    # TODO: ajoutez le code
    pass
