# Labo 09 – Récapitulation des sujets du cours, bases de données distribuées

<img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Ets_quebec_logo.png" width="250">    
ÉTS - LOG430 - Architecture logicielle - Chargé de laboratoire: Gabriel C. Ullmann.

## 🎯 Objectifs d'apprentissage
- Créer un projet Flask Python conteneurisé avec base de données à partir de zéro
- Utiliser [Apache Cassandra](https://cassandra.apache.org/doc/latest/cassandra/architecture/overview.html) pour effectuer des opérations simples d'écriture et de lecture
- Comprendre les principes des transactions distribuées et de la réplication

## ⚙️ Setup

Avec le labo 09, nous concluons le processus d'évolution architecturale et fonctionnelle de l'application StoreManager. Nous sommes partis d'une application de gestion de magasin très simple et avons fait évoluer son architecture d'un monolithe vers des microservices event-driven. 

La prochaine étape consiste à migrer notre application vers le nuage et à la préparer pour un fonctionnement entièrement distribué, y compris au niveau de la base de données. Concrètement, au lieu que chaque service possède sa propre base de données et que nous gérions manuellement la synchronisation entre ces différentes bases, nous utiliserons une base de données qui assure elle-même cette distribution et cette synchronisation. Apache Cassandra est un exemple de ce type de base de données distribuée, et nous apprendrons comment l'utiliser.

Pour ajouter un défi supplémentaire dans cette implémentation, nous n'utiliserons pas une structure prédéfinie comme dans les labos précédents. Aujourd'hui, vous allez créer la structure vous-même à partir de zéro, en créant le `requirements.txt`, `Dockerfile`, `docker-compose.yml`, `.env`, `config.py` et `db.py`. Chaque activité vous guidera dans une étape de setup, puis l'implémentation.

### 1. Clonez le dépôt
Créez votre propre dépôt à partir du dépôt gabarit (template). Vous pouvez modifier la visibilité pour le rendre privé si vous voulez.
```bash
git clone https://github.com/[votrenom]/log430-labo9
cd log430-labo9
```

> 📝 NOTE : même si l'architecture de cette application est très similaire au labo 3 (une API REST), je vous recommande de lire les documents arc42 et ADR dans le fichier `docs` avant de commencer les activités. Il existe de petites différences par rapport au labo 3, par exemple l'utilisation des DAOs plutôt que d'un ORM.

## 🧪 Activités pratiques

### 1. Créez votre fichier requirements.txt
Vous aurez besoin des dépendances suivantes pour ce projet :
- `cassandra-driver>=3.29` : pour la connexion à Cassandra
- `python-dotenv>=1.0` : pour la gestion des variables d'environnement
- `Flask>=2.0` : pour les endpoints API
- `requests>=2.0` : pour les requêtes HTTP
- `pytest>=7.0` : pour les tests unitaires

### 2. Créez votre Dockerfile
Créez un `Dockerfile` qui utilise l'image `python:3.11-slim`, comme nous l'avons utilisée lors des derniers labos.

```dockerfile
FROM python:3.11-slim
WORKDIR /app/src

# TODO: Écrivez la commande qui copie requirements.txt de votre ordinateur au conteneur et installez les dépendances
# TODO: Écrivez la commande qui copie le code de l'application de votre ordinateur au conteneur
# Démarrez votre API
CMD ["python", "api.py"]
```

### 3. Créez votre docker-compose.yml
Créez un fichier `docker-compose.yml` avec 2 services : `store_manager` et `cassandra`. Pour Cassandra, utilisez la version 4.1 de l'image officielle disponible sur [Docker Hub](https://hub.docker.com/_/cassandra). Pour `store_manager`, utilisez le même port que nous avons utilisé pendant les labos précédents (5000).

```yaml
services:
  cassandra:
    image: cassandra:4.1
    container_name: cassandra
    environment:
      - CASSANDRA_CLUSTER_NAME=StoreManagerCluster
      - CASSANDRA_AUTHENTICATOR=PasswordAuthenticator
      - CASSANDRA_AUTHORIZER=CassandraAuthorizer

  store_manager:
    build: .
    # TODO: Ouvrez le port pour nous permettre d'y accéder hors Docker via Postman 
    volumes:
      - .:/app
    depends_on:
      - cassandra
```

### 4. Ajoutez un healthcheck au conteneur Cassandra
Dans le fichier `docker-compose.yml`, ajoutez l'attribut `healthcheck` dans le service `cassandra` pour vous assurer qu'il est bien démarré avant l'initialisation du `store_manager`. Sans le `healthcheck`, le `store_manager` pourrait quand même fonctionner et faire la connexion avec Cassandra quelques fois, mais les vérifications répétées peuvent nous garantir que cela fonctionnera toujours.

Cassandra:
```yaml
    healthcheck:
      test: ["CMD-SHELL", "nodetool status | grep -E '^UN'"]
      interval: 15s
      timeout: 10s
      retries: 40
      start_period: 60s
```

Store Manager:
```yaml
    depends_on:
      cassandra:
        condition: service_healthy
```

### 5. Créez vos fichiers .env

Créez un fichier `.env` à partir du .env.example :
```
CASSANDRA_HOST=cassandra
CASSANDRA_USERNAME=labo09
CASSANDRA_PASSWORD=labo09
```

### 6. Créez votre script de configuration
Dans `src/config.py`, créez un script pour lire votre fichier `.env` en utilisant `python-dotenv` et charger les variables en mémoire pour les utiliser dans l'API plus tard.

```python
import os
from dotenv import load_dotenv

load_dotenv()

# TODO: Créez des variables pour stocker TOUTES les valeurs de configuration
# Exemple: CASSANDRA_HOST = os.getenv('CASSANDRA_HOST')
```

### 7. Créez votre application Flask et connectez-vous à Cassandra
Dans `src/db.py`, écrivez le code pour vous connecter à Cassandra. Lisez l'username, le password et l'host **à partir de la configuration**. Il ne faut pas mettre les informations de connexion hardcoded.

```python
def get_cassandra_connection():
    """Connect to Cassandra"""
    try:
        auth_provider = PlainTextAuthProvider(username='TODO_USERNAME_ICI', password='TODO_PASSWORD_ICI')
        cluster = Cluster(['TODO_HOST_ICI'], auth_provider=auth_provider)
        session = cluster.connect()
        return cluster, session
    except Exception as e:
        logger.error(e)
        raise e
```

> 📝 NOTE : il n'y a pas besoin de conserver le mot `pass` dans le code, ce mot-là est simplement un placeholder pour permettre d'exécuter une méthode même quand nous n'avons pas de code.

Démarrez vos conteneurs et vérifiez que la connexion fonctionne :

```bash
docker compose build
docker compose up -d
```

### 8. Créez votre keyspace

Un keyspace dans Cassandra est l'équivalent d'une base de données dans les systèmes relationnels. Il définit la stratégie de réplication des données à travers le cluster.

Ajoutez une fonction dans `db.py` pour créer le keyspace avec 1 replica, et 1 table `products` pour assurer la persistance des articles du magasin :

```python
def setup_database():
    """Setup keystores and tables"""
    cluster, session = get_cassandra_connection()
    session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS store_manager
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
    """
    )
    logger.info("Keyspace 'store_manager' created")
    session.set_keyspace("store_manager")
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id UUID PRIMARY KEY,
            name VARCHAR,
            sku VARCHAR,
            price DECIMAL
        )
    """
    )
    logger.info("Table 'products' created")
    session.shutdown()
    cluster.shutdown()
```

### 9. Ajoutez un endpoint pour créer un article

Créez un endpoint REST pour ajouter des articles à la base de données. 

- Pour l'implémentation : utilisez l'exemple suivant, générez un uuid en utilisant des fonctions natives Python et écrivez le INSERT en utilisant un [prepared statement](https://docs.datastax.com/en/developer/python-driver/3.29/getting_started/index.html#prepared-statement)
- Pour organiser votre code : Utilisez les patrons MVC et DAO.

Par exemple, dans `src/api.py`:
```python
@app.post('/products')
def post_product():
    """Create a new product based on user inputs"""
    controller = ProductController()
    return controller.create_product(request)
```

Dans `src/controllers/product_controller.py`:
```python
def create_product(self, request):
    """ Create a new product based on user inputs """
    payload = request.get_json()
    name = payload.get('name')
    sku = payload.get('sku')
    price = payload.get('price')
    try:
      # Validez vos paramètres
      # Générez un uuid en utilisant des fonctions natives Python
      # Créez une nouvelle instance de la classe Product
      # Appelez la méthode insert dans product_dao
      return jsonify({'uuid': new_uuid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        self.dao.close()
```

Dans `src/daos/product_dao.py`:
```python
  def insert(self, product):
      """ Insert given product into Casandra """
      # TODO: ajoutez l'article dans la base de données
      self.logger.info(product)
```

Implémentez la logique pour insérer un article dans Cassandra. Ensuite, exécutez les tests unitaires, au moins le test d'écriture devrait passer.

> 📝 REMARQUE : Cassandra utilise l'algorithme [Paxos](https://docs.datastax.com/en/dse/6.9/architecture/database-internals/lightweight-transactions.html) pour gérer les transactions distribuées. Par exemple, si deux nœuds Cassandra distincts reçoivent simultanément une demande de soustraire 100 unités d'un produit de l'inventaire, un seul peut le faire. C'est grâce à l'algorithme Paxos que les nœuds parviennent à un consensus sur celui qui doit effectuer l'opération. Sans Paxos, dans une telle situation, 200 unités seraient déduites de l'inventaire.

### 10. Ajoutez un endpoint pour lire les articles

Créez un endpoint pour [récupérer tous les articles](https://docs.datastax.com/en/developer/python-driver/3.29/getting_started/index.html#executing-queries) . Suivez la même sequence d'appels que l'activité 10 (Controller -> Model -> DAO).

```python
@app.get('/products')
def get_products():
    """Get all products"""
    controller = ProductController()
    return controller.list_products()
```

Exécutez les tests unitaires, les tests d'écriture et de lecture devront passer.

### 11. Testez la distribution des données

Pour cette activité bonus, vous allez expérimenter avec la distribution des données dans un cluster Cassandra multi-nœuds.

#### Configuration d'un cluster multi-nœuds

Modifiez votre `docker-compose.yml` pour ajouter deux nœuds Cassandra supplémentaires :

```yaml
services:
  cassandra-2:
    image: cassandra:4.1
    container_name: cassandra-2
    environment:
      - CASSANDRA_CLUSTER_NAME=StoreManagerCluster
      - CASSANDRA_SEEDS=cassandra
      - CASSANDRA_AUTHENTICATOR=PasswordAuthenticator
      - CASSANDRA_AUTHORIZER=CassandraAuthorizer
    depends_on:
      - cassandra
    healthcheck:
      test: ["CMD-SHELL", "nodetool status | grep -E '^UN'"]
      interval: 15s
      timeout: 10s
      retries: 40
      start_period: 60s
```

#### Modifiez la stratégie de réplication

Modifiez votre keyspace dans `db.py` pour utiliser un facteur de réplication de 2 :

```python
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS store_manager
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '2'}
""")
```

Modifiez le fichier `.env`:
```sh
CASSANDRA_HOST=cassandra,cassandra-2
```

Modifiez le fichier `config.py` pour lire un array de hostnames:
```py
CASSANDRA_HOSTS = os.getenv("CASSANDRA_HOST").split(",")
```

Modifiez le fichier `db.py`:
```py
cluster = Cluster(config.CASSANDRA_HOST, auth_provider=auth_provider)
```

Récréez la base de donées et les conteneurs.

#### Testez la résilience
- Insérez plusieurs articles via votre API
- Arrêtez un des conteneurs (par example, `cassandra`) 
- Vérifiez que vous pouvez toujours lire les données
- Redémarrez le conteneur et vérifiez que les données sont synchronisées

#### Questions pour réflechir
- Comment le facteur de réplication affecte-t-il la disponibilité et la cohérence des données ?
- Quels sont les compromis entre performance et résilience ?

## 📦 Livrables

- Un fichier .zip contenant l'intégralité du code source du projet Labo 09.
