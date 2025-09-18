import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Pega os valores das variáveis
user = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")
cluster = os.getenv("MONGO_CLUSTER")
db_name = os.getenv("MONGO_DB")

# Cria a conexão com o MongoDB
client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0")

# Seleciona o banco
db = client[db_name]

# Coleções
collection_participantes = db["participantes"]
collection_palestrantes = db["palestrantes"]
collection_organizadores = db["organizadores"]
collection_patrocinadores = db["patrocinadores"]
collection_eventos = db["eventos"]