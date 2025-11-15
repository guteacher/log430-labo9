# Labo 09 – Récapitulation des sujets du cours, bases de données distribuées

<img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Ets_quebec_logo.png" width="250">    
ÉTS - LOG430 - Architecture logicielle - Chargé de laboratoire: Gabriel C. Ullmann, Automne 2025.

## 🎯 Objectifs d'apprentissage
- Créer un projet Flask Python avec base de données conteneurisé à partir de zéro
- Utiliser Apache Cassandra pour effectuer des opérations simples d'écriture et de lecture
- Comprendre les principes des bases de données distribuées et leur réplication

## ⚙️ Setup

Le labo 09 est la fin d'un processus où nous avons commencé avec une application de gestion de magasin - Store Manager - très simple et nous avons évolué son architecture d'un monolithe jusqu'aux microservices event-driven. La prochaine étape serait apporter notre application au nuage, et la préparer pour travailler de manière complètement distribuée, incluant la base de données. Cela signifie qu'au lieu d'avoir chaque service avec sa propre base de données et faire la synchronisation entre différentes bases à la main, nous utilisons une base de données qui elle-même fait cette distribution et synchronisation.

Pour ajouter un défi supplémentaire dans cette implémentation, nous n'utiliserons pas une structure prédéfinie comme dans les labos précédents. Aujourd'hui, vous allez créer la structure vous-même à partir de zéro, en créant le `Dockerfile`, `docker-compose.yml`, `.env`, `config`, etc. Chaque activité vous guidera dans une étape de setup, puis l'implémentation.

### 1. Clonez le dépôt
Créez votre propre dépôt à partir du dépôt gabarit (template). Vous pouvez modifier la visibilité pour le rendre privé si vous voulez.
```bash
git clone https://github.com/[votrenom]/log430-labo9
cd log430-labo9
```

> ⚠️ Arc42

## 🧪 Activités pratiques

### 1. Créez votre fichier requirements.txt
Vous aurez besoin des dépendances suivantes pour ce projet :
- `cassandra-driver>=3.29` : pour la connexion à Cassandra
- `python-dotenv>=1.0` : pour la gestion des variables d'environnement
- `Flask>=2.0` : pour l'application web

### 2. Créez votre Dockerfile
Créez un `Dockerfile` qui utilise l'image `python:3.11-slim`, tel que nous avons utilisé pendant les derniers labos.

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# TODO: Copiez requirements.txt de votre ordinateur au conteneur et installez les dépendances
# TODO: Copiez le code de l'application de votre ordinateur au conteneur
# TODO: Exposez le port 5000
# Démarrez votre API
CMD ["python", "src/api.py"]
```

### 3. Créez votre docker-compose.yml
Créez un fichier `docker-compose.yml` avec 2 services : `store_manager-service` et `cassandra`. Pour Cassandra, utilisez la version 4.1 de l'image officielle disponible sur [Docker Hub](https://hub.docker.com/_/cassandra) et ouvrez le port 9042. Pour `store_manager-service`, utilisez le même port que nous avons utilisé pendant les labos précédents (5000).

```yaml
# TODO: Ouvrez les ports nécéssaires
services:
  cassandra:
    image: cassandra:4.1
    environment:
      - CASSANDRA_CLUSTER_NAME=store_managerCluster
      - CASSANDRA_DC=datacenter1
      - CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch
      - CASSANDRA_AUTHENTICATOR=PasswordAuthenticator
      - CASSANDRA_AUTHORIZER=CassandraAuthorizer

    store_manager-service:
      build: .
      depends_on:
        - cassandra
```

### 5. Créez vos fichiers .env 
Créez un fichier `.env` à partir du .env.example :
```
CASSANDRA_HOST=cassandra
CASSANDRA_USERNAME=labo09
CASSANDRA_PASSWORD=labo09
```

### 6. Créez votre script de configuration
Dans `src/config.py`, créez un script pour lire votre fichier `.env` en utilisant `python-dotenv` et mettre les variables dans la mémoire pour les utiliser dans l'API plus tard.

```python
import os
from dotenv import load_dotenv

load_dotenv()

# TODO: Créez des variables pour stocker TOUS les valeurs de configuration
# Exemple: CASSANDRA_HOST = os.getenv('CASSANDRA_HOST') 
```

### 7. Créez votre application Flask et connectez-vous à Cassandra
Dans `src/db.py`, écrivez le code pour créer une application Flask et vous connecter à Cassandra. Lisez l'username, password et host **à partir du config**. Il ne faut pas mettre les informations de connexion hardcoded.

```python
def get_cassandra_connection():
  try:
      auth_provider = PlainTextAuthProvider(username='TODO_USERNAME_ICI', password='TODO_PASSWORD_ICI')
      cluster = Cluster(['TODO_HOST_ICI'], auth_provider=auth_provider)
      session = cluster.connect()
      return cluster, session
  except Exception as e:
      raise e
```

Démarrez vos conteneurs et vérifiez que la connexion fonctionne :
```bash
docker compose build
docker compose up -d
```

### 8. Créez votre keyspace
Un keyspace dans Cassandra est l'équivalent d'une base de données dans les systèmes relationnels. Il définit la stratégie de réplication des données à travers le cluster.

Ajoutez une fonction dans `db.py` pour créer le keyspace avec 1 replica:

```python
def setup_database():
    """Create a keyspace with a replication strategy, and a table"""
    cluster, session = get_cassandra_connection()
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS store_manager 
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
    """)
    print("✅ Keyspace 'store_manager' created")
    
    # Use the keyspace
    session.set_keyspace('store_manager')
    
    # Create table
    session.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id UUID PRIMARY KEY,
            name VARCHAR(150),
            sku VARCHAR(64),
            price DECIMAL(10,2)
        )
    """)
```

### 10. Ajoutez un endpoint pour créer un produit
Créez un endpoint REST pour ajouter des produits à la base de données.

```python
@app.route('/products', methods=['POST'])
def create_product():
    """Crée un nouveau produit"""
    data = request.get_json()
    
    # TODO: Validez les données reçues
    # TODO: Générez un UUID pour le product_id
    # TODO: Insérez le produit dans Cassandra
    # TODO: Retournez une réponse appropriée
    
    pass
```

Implémentez la logique pour insérer un produit dans Cassandra. Ensuite, executez les tests unitaires, au moins le test de écriture devrait passer.

### 11. Ajoutez un endpoint pour lire les produits
Créez un endpoint pour récupérer tous les produits.

```python
@app.route('/products', methods=['GET'])
def get_products():
    """Récupère tous les produits"""
    # TODO: Exécutez une requête SELECT
    # TODO: Transformez les résultats en format JSON
    # TODO: Retournez la liste des produits
    pass
```

Executez les tests unitaires, le test de écriture et lecture devront passer.

### 12. Testez la distribution des données (Bonus)
Modifiez votre `docker-compose.yml` pour ajouter un deuxième nœud Cassandra :

```yaml
  cassandra-node2:
    image: cassandra:latest
    environment:
      - CASSANDRA_SEEDS=cassandra
      # TODO: Ajoutez les autres configurations
```

Changez la stratégie de réplication pour utiliser `replication_factor = 2` et observez comment les données sont répliquées automatiquement entre les nœuds.

## 📦 Livrables

- Un fichier .zip contenant l'intégralité du code source du projet Labo 09.
