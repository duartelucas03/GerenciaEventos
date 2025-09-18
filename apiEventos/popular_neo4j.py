import os
from dotenv import load_dotenv
from pymongo import MongoClient
from neo4j import GraphDatabase

from database import (
    collection_participantes,
    collection_palestrantes,
    collection_organizadores,
    collection_patrocinadores,
    collection_eventos,
)

# Carregar variáveis do .env
load_dotenv(dotenv_path=r"C:\Users\lucas\Área de Trabalho\UFU\7o período\NOSQL\Trab_NoSQL\.env")
senha = os.getenv("NEO4J_PASSWORD")

# Conexão com Neo4j
neo4j_driver = GraphDatabase.driver(
    "neo4j://127.0.0.1:7687",
    auth=("neo4j", senha)
)

def criar_no_e_relacoes():
    with neo4j_driver.session() as session:

        # Limpa o banco (opcional)
        session.run("MATCH (n) DETACH DELETE n")

        # --- Criar Organizadores ---
        for org in collection_organizadores.find():
            session.run("""
                MERGE (o:Organizador {nome: $nome})
                SET o.telefone = $telefone, o.cpf = $cpf
            """, {
                "nome": org.get("nome", "Desconhecido"),
                "telefone": org.get("telefone", "N/A"),
                "cpf": str(org.get("cpf", "SEM-CPF"))
            })

        # --- Criar Palestrantes ---
        for pal in collection_palestrantes.find():
            session.run("""
                MERGE (pal:Palestrante {nome: $nome})
                SET pal.telefone = $telefone, pal.cpf = $cpf
            """, {
                "nome": pal.get("nome", "Desconhecido"),
                "telefone": pal.get("telefone", "N/A"),
                "cpf": str(pal.get("cpf", "SEM-CPF"))
            })

        # --- Criar Patrocinadores ---
        for pat in collection_patrocinadores.find():
            session.run("""
                MERGE (pat:Patrocinador {nome: $nome})
                SET pat.telefone = $telefone, pat.cnpj = $cnpj, pat.valor_investido = $valor
            """, {
                "nome": pat.get("nome", "Desconhecido"),
                "telefone": pat.get("telefone", "N/A"),
                "cnpj": str(pat.get("cnpj", "SEM-CNPJ")),
                "valor": pat.get("valor_investido", 0.0)
            })

        # --- Criar Eventos e relacionamentos ---
        for ev in collection_eventos.find():
            ev_nome = ev.get("nome", "Sem Nome")
            ev_id = str(ev.get("id", "SEM-ID"))

            session.run("""
                MERGE (e:Evento {nome: $nome})
                SET e.id = $id, e.data = $data, e.local = $local, e.descricao = $descricao, e.limite = $limite
            """, {
                "nome": ev_nome,
                "id": ev_id,
                "data": ev.get("data", "Sem Data"),
                "local": ev.get("local", "Local Indefinido"),
                "descricao": ev.get("descricao", "Sem Descrição"),
                "limite": ev.get("limite", 0)
            })

            # Organizador -> Evento
            organizador = ev.get("organizador")
            if organizador:
                nome_org = organizador.get("nome") if isinstance(organizador, dict) else str(organizador)
                result = session.run("""
                    MATCH (o:Organizador {nome: $nome_org}), (e:Evento {nome: $ev_nome})
                    MERGE (o)-[:ORGANIZA]->(e)
                """, {"nome_org": nome_org, "ev_nome": ev_nome})
                print(f"Relacionamento ORGANIZA criado: {nome_org} -> {ev_nome}")

            # Palestrantes -> Evento
            palestrs = ev.get("palestrantes", [])
            if not isinstance(palestrs, list):
                palestrs = [palestrs]
            for pal in palestrs:
                nome_pal = pal.get("nome") if isinstance(pal, dict) else str(pal)
                session.run("""
                    MATCH (pal:Palestrante {nome: $nome_pal}), (e:Evento {nome: $ev_nome})
                    MERGE (pal)-[:PALESTRA_EM]->(e)
                """, {"nome_pal": nome_pal, "ev_nome": ev_nome})
                print(f"Relacionamento PALESTRA_EM criado: {nome_pal} -> {ev_nome}")

            # Patrocinadores -> Evento
            pats = ev.get("patrocinadores", [])
            if not isinstance(pats, list):
                pats = [pats]
            for pat in pats:
                nome_pat = pat.get("nome") if isinstance(pat, dict) else str(pat)
                session.run("""
                    MATCH (pat:Patrocinador {nome: $nome_pat}), (e:Evento {nome: $ev_nome})
                    MERGE (pat)-[:PATROCINA]->(e)
                """, {"nome_pat": nome_pat, "ev_nome": ev_nome})
                print(f"Relacionamento PATROCINA criado: {nome_pat} -> {ev_nome}")

        # --- Criar Participantes e relacionamentos ---
        for p in collection_participantes.find():
            cpf_part = str(p.get("cpf", f"SEM-CPF-{p.get('_id')}"))
            nome_part = p.get("nome", "Desconhecido")
            telefone_part = p.get("telefone", "N/A")
            curso_part = p.get("curso", "Não informado")

            # Cria nó do participante
            session.run("""
                MERGE (p:Participante {cpf: $cpf})
                SET p.nome = $nome, p.telefone = $telefone, p.curso = $curso
            """, {"cpf": cpf_part, "nome": nome_part, "telefone": telefone_part, "curso": curso_part})

            # Criar relacionamento PARTICIPA
            eventos_part = p.get("evento", [])
            if isinstance(eventos_part, str):
                eventos_part = [eventos_part]
            elif not isinstance(eventos_part, list):
                eventos_part = []

            # Filtra apenas eventos válidos
            eventos_part = [ev_nome for ev_nome in eventos_part if ev_nome]

            for ev_nome in eventos_part:
                # Verifica se o evento existe
                check = session.run("MATCH (e:Evento {nome: $ev_nome}) RETURN e", {"ev_nome": ev_nome})
                if check.single():
                    session.run("""
                        MATCH (p:Participante {cpf: $cpf})
                        MATCH (e:Evento {nome: $ev_nome})
                        MERGE (p)-[:PARTICIPA]->(e)
                    """, {"cpf": cpf_part, "ev_nome": ev_nome})
                    print(f"Relacionamento PARTICIPA criado: {nome_part} -> {ev_nome}")
                else:
                    print(f"Aviso: evento '{ev_nome}' do participante '{nome_part}' não existe no Neo4j")

    print("Banco Neo4j populado com sucesso!")

if __name__ == "__main__":
    criar_no_e_relacoes()
