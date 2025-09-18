from graphdatascience import GraphDataScience
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()
senha = os.getenv("NEO4J_PASSWORD")

# Conexão com Neo4j
neo4j_driver = GraphDatabase.driver(
    "neo4j://127.0.0.1:7687",
    auth=("neo4j", senha)
)

gds = GraphDataScience("neo4j://127.0.0.1:7687", auth=("neo4j", senha))
print("Versão do GDS:", gds.version())

# Remove o grafo se ele já existir
if "eventos_graph" in gds.graph.list()["graphName"].values:
    gds.graph.drop("eventos_graph")

# Cria o grafo novamente
gds.graph.project(
    "eventos_graph",
    node_spec=["Participante", "Evento", "Palestrante", "Organizador", "Patrocinador"],
    relationship_spec=["PARTICIPA", "ORGANIZA", "PALESTRA_EM", "PATROCINA"]
)

# Obtém o objeto Graph
eventos_graph = gds.graph.get("eventos_graph")

# Executa PageRank
result = gds.pageRank.stream(eventos_graph)

# Converte para DataFrame
df = result.copy()  # já é um DataFrame

# Pega nomes e labels (rótulos) dos nós via Neo4j
with neo4j_driver.session() as session:
    query = """
    MATCH (n)
    WHERE id(n) IN $ids
    RETURN id(n) AS nodeId, n.nome AS nome, labels(n) AS labels
    """
    res = session.run(query, ids=[int(i) for i in df['nodeId']])
    node_info = {record['nodeId']: {'nome': record['nome'], 'labels': record['labels']} for record in res}

# Adiciona nomes e labels ao DataFrame
df['nome'] = df['nodeId'].map(lambda x: node_info[x]['nome'] if x in node_info else 'Desconhecido')
df['labels'] = df['nodeId'].map(lambda x: node_info[x]['labels'] if x in node_info else [])

# Filtra apenas nós com label 'Evento'
df_eventos = df[df['labels'].apply(lambda lbls: 'Evento' in lbls)]

# Ordena pelo PageRank
df_eventos = df_eventos.sort_values(by='score', ascending=False)

# Exibe resultados
print(df_eventos[['nodeId', 'nome', 'score']])
