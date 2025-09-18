from fastapi import FastAPI, HTTPException, Path
from database import collection_participantes
from database import collection_palestrantes
from database import collection_organizadores
from database import collection_patrocinadores
from database import collection_eventos
import redis
import json
from cache import get_cache, set_cache  # usa funções do cache.py
from models import Participante, Evento, Organizador, Palestrante, Patrocinador

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from typing import Optional, List


app = FastAPI()


# --- CORS (permita o front dev server) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],  # troque "*" por origens específicas em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- helpers ---
def serialize_doc(doc):
    if not doc: 
        return None
    d = dict(doc)
    if "_id" in d:
        d["_id"] = str(d["_id"])
    return d


# --- Pydantic models para validação de entrada ---
class ParticipanteIn(BaseModel):
    nome: str
    cpf: str
    telefone: Optional[str] = None
    curso: Optional[str] = None
    evento: Optional[List[str]] = []

class EventoIn(BaseModel):
    nome: str
    data: Optional[str] = None
    local: Optional[str] = None
    descricao: Optional[str] = None
    cpf_organizador: str
    palestrantes_cpf: Optional[List[str]] = []
    patrocinadores_cnpj: Optional[List[str]] = []


class OrganizadorIn(BaseModel):
    nome: str
    telefone: str
    cpf: str

class PalestranteIn(BaseModel):
    nome: str
    telefone: str
    cpf: str

class PatrocinadorIn(BaseModel):
    nome: str
    telefone: str
    cnpj: str
    valorInvestido: float

class InscricaoIn(BaseModel):
    cpf: str

class CancelarIn(BaseModel):
    cpf_participante: str
    nome_evento: str

class AtualizarEventoIn(BaseModel):
    cpfs_palestrantes: Optional[List[str]] = []
    cnpjs_patrocinadores: Optional[List[str]] = []



@app.get("/")
def home():
    return {"mensagem": "API de Eventos Acadêmicos"}

@app.get("/participante/{cpf}")
def buscar_participante_por_cpf(cpf: str):
    participante = collection_participantes.find_one({"cpf": cpf})
    if not participante:
        raise HTTPException(status_code=404, detail="Participante não encontrado")

    participante["_id"] = str(participante["_id"])  # Serializar o ID

    cache.pfadd("participantes_hll", cpf)

    return participante

@app.get("/palestrante/{cpf}")
def buscar_palestrante_por_cpf(cpf: str):
    palestrante = collection_palestrantes.find_one({"cpf": cpf})
    if not palestrante:
        raise HTTPException(status_code=404, detail="Palestrante não encontrado")

    palestrante["_id"] = str(palestrante["_id"])  # Serializar o ID
    return palestrante

@app.get("/organizador/{cpf}")
def buscar_organizador_por_cpf(cpf: str):
    organizador = collection_organizadores.find_one({"cpf": cpf})
    if not organizador:
        raise HTTPException(status_code=404, detail="Organizador não encontrado")

    organizador["_id"] = str(organizador["_id"])  # Serializar o ID
    return organizador

@app.get("/patrocinador/{cnpj}")
def buscar_patrocinador_por_cnpj(cnpj: str):
    patrocinador = collection_patrocinadores.find_one({"cnpj": cnpj})
    if not patrocinador:
        raise HTTPException(status_code=404, detail="Patrocinador não encontrado")

    patrocinador["_id"] = str(patrocinador["_id"])  # Serializar o ID
    return patrocinador

@app.get("/evento/{id}")
def buscar_evento_por_id(id: int):
    evento = collection_eventos.find_one({"id": id})
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    evento["_id"] = str(evento["_id"])  # Serializar o ID
    return evento


@app.get("/eventos/participantes")
def listar_eventos_com_total_participantes():
    pipeline = [
        {
            "$project": {
                "nome": 1,
                "data": 1,
                "total_participantes": "$participantes"  # já usa o campo existente
            }
        },
        {"$sort": {"total_participantes": -1}}
    ]

    resultado = list(collection_eventos.aggregate(pipeline))

    for doc in resultado:
        doc["_id"] = str(doc["_id"])

    return resultado



@app.get("/organizadores/eventos-estatisticas")
def estatisticas_organizadores():
    pipeline = [
        {
            "$group": {
                "_id": "$organizador",
                "quantidade_eventos": {"$sum": 1},
                "total_participantes": {"$sum": "$participantes"}
            }
        },
        {
            "$project": {
                "organizador": "$_id",
                "quantidade_eventos": 1,
                "total_participantes": 1,
                "_id": 0
            }
        },
        {
            "$sort": {"total_participantes": -1}
        }
    ]

    resultado = list(collection_eventos.aggregate(pipeline))

    return resultado
'''
@app.get("/participantes/eventos")
def eventos_por_participante():
    pipeline = [
        {
            "$group": {
                "_id": {
                    "nome": "$nome",
                    "cpf": "$cpf"
                },
                "eventos": {
                    "$addToSet": "$evento"
                }
            }
        },
        {
            "$project": {
                "nome": "$_id.nome",
                "cpf": "$_id.cpf",
                "eventos": 1,
                "_id": 0
            }
        },
        {
            "$sort": {
                "nome": 1
            }
        }
    ]

    resultado = list(collection_participantes.aggregate(pipeline))

    return resultado
'''

# conexão com Redis
cache = redis.Redis(host="localhost", port=6380, decode_responses=True)

@app.get("/participantes/eventos")
def eventos_por_participante():
    cache_key = "participantes_eventos"

    # tenta pegar do cache
    cached = cache.get(cache_key)
    if cached:
        return {"from_cache": True, "data": json.loads(cached)}

    # se não tem no cache, busca no Mongo
    pipeline = [
        {
            "$group": {
                "_id": {"nome": "$nome", "cpf": "$cpf"},
                "eventos": {"$addToSet": "$evento"}
            }
        },
        {
            "$project": {
                "nome": "$_id.nome",
                "cpf": "$_id.cpf",
                "eventos": 1,
                "_id": 0
            }
        },
        {"$sort": {"nome": 1}}
    ]

    resultado = list(collection_participantes.aggregate(pipeline))

    # salva no Redis
    cache.setex(cache_key, 120, json.dumps(resultado))

    return {"from_cache": False, "data": resultado}


# estrutura avançada HyperLogLog

# rota para contar participantes únicos
@app.get("/participantes/contagem-unica")
def contar_participantes_unicos():
    count = cache.pfcount("participantes_hll")
    return {"participantes_unicos": count}


# NOVOS ENDPOINTS

@app.get("/eventos")
def listar_eventos():
    docs = list(collection_eventos.find())
    return [serialize_doc(d) for d in docs]

@app.post("/eventos")
def criar_evento(ev: EventoIn):
    """
    Cria um evento. Campos esperados:
      - nome, data, local, descricao, limite (int)
      - cpf_organizador (obrigatório; organización deve já existir)
      - palestrantes_cpfs (lista de CPFs; serão convertidos para nomes se existirem)
      - patrocinadores_cnpjs (lista de CNPJs; serão convertidos para nomes se existirem)
    O documento armazenado inclui:
      - id (inteiro incremental), nome, data, local, descricao, limite
      - participantes (contador inicial 0)
      - organizador (CPF) e organizador_nome (para conveniência)
      - palestrantes (lista de nomes), patrocinadores (lista de nomes)
    """
    # valida organizador
    org_doc = collection_organizadores.find_one({"cpf": ev.cpf_organizador})
    if not org_doc:
        raise HTTPException(status_code=400, detail="Organizador (CPF) não encontrado. Cadastre o organizador primeiro.")

    # calcula próximo id (mesma lógica do menu)
    ultimo = collection_eventos.find_one(sort=[("id", -1)], projection={"id": 1, "_id": 0})
    proximo_id = (ultimo["id"] + 1) if (ultimo and "id" in ultimo) else 1

    # resolve palestrantes por CPF -> nome (se existir)
    palestrantes_nomes = []
    for cpf in ev.palestrantes_cpf or []:
        pal = collection_palestrantes.find_one({"cpf": cpf})
        if pal:
            palestrantes_nomes.append(pal.get("nome"))

    # resolve patrocinadores por CNPJ -> nome (se existir)
    patrocinadores_nomes = []
    for cnpj in ev.patrocinadores_cnpj or []:
        pat = collection_patrocinadores.find_one({"cnpj": cnpj})
        if pat:
            patrocinadores_nomes.append(pat.get("nome"))

    evento_doc = {
        "id": proximo_id,
        "nome": ev.nome,
        "data": ev.data,
        "local": ev.local,
        "descricao": ev.descricao,
        "participantes": 0,                   
        "organizador": org_doc.get("nome"),   
        "palestrantes": palestrantes_nomes,
        "patrocinadores": patrocinadores_nomes
    }

    res = collection_eventos.insert_one(evento_doc)
    return {"status": "created", "id": proximo_id, "_id": str(res.inserted_id)}

@app.get("/participantes")
def listar_participantes():
    docs = list(collection_participantes.find())
    return [serialize_doc(d) for d in docs]

@app.post("/participantes")
def criar_participante(p: ParticipanteIn):
    """
    Cadastra (ou ignora se já existe) um participante usando CPF como chave.
    Campos: nome, cpf, telefone (opcional), curso (opcional).
    """
    res = collection_participantes.update_one(
        {"cpf": p.cpf},
        {"$setOnInsert": {"nome": p.nome, "telefone": p.telefone, "cpf": p.cpf, "curso": p.curso}},
        upsert=True
    )
    if getattr(res, "upserted_id", None):
        return {"status": "created", "cpf": p.cpf}
    return {"status": "exists", "cpf": p.cpf}


@app.post("/eventos/{evento_id}/inscrever")
def inscrever_participante(evento_id: int = Path(..., description="ID numérico do evento"), inscricao: InscricaoIn = None):
    """
    Inscreve um participante (por CPF) num evento identificado pelo campo numérico 'id'.
    Comportamento (conforme popular_menu.py):
      - adiciona o nome do evento ao array 'evento' do participante ($addToSet)
      - incrementa o contador 'participantes' do evento
      - verifica duplicidade (não inscreve duas vezes)
      - verifica limite (se definido) e impede inscrição se cheio
    """
    cpf = inscricao.cpf.strip()
    part_doc = collection_participantes.find_one({"cpf": cpf})
    if not part_doc:
        raise HTTPException(status_code=404, detail="Participante não encontrado")

    event_doc = collection_eventos.find_one({"id": evento_id})
    if not event_doc:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    nome_evento = event_doc.get("nome")

    # Checa se já inscrito (popular_menu usa 'evento' no participante para armazenar nomes)
    if nome_evento in part_doc.get("evento", []):
        raise HTTPException(status_code=400, detail="Participante já inscrito neste evento")

    # adiciona o evento ao participante
    collection_participantes.update_one({"cpf": cpf}, {"$addToSet": {"evento": nome_evento}})

    # incrementa contador de participantes no evento
    collection_eventos.update_one({"id": evento_id}, {"$inc": {"participantes": 1}})

    return {"status": "ok", "evento": nome_evento, "cpf": cpf}


@app.post("/organizadores")
def adicionar_organizador(org: OrganizadorIn):
    if collection_organizadores.find_one({"cpf": org.cpf}):
        raise HTTPException(status_code=400, detail="Organizador já cadastrado")
    collection_organizadores.insert_one(org.dict())
    return {"msg": f"Organizador {org.nome} adicionado!"}


@app.post("/palestrantes")
def adicionar_palestrante(pal: PalestranteIn):
    if collection_palestrantes.find_one({"cpf": pal.cpf}):
        raise HTTPException(status_code=400, detail="Palestrante já cadastrado")
    collection_palestrantes.insert_one(pal.dict())
    return {"msg": f"Palestrante {pal.nome} adicionado!"}


@app.post("/patrocinadores")
def adicionar_patrocinador(pat: PatrocinadorIn):
    if collection_patrocinadores.find_one({"cnpj": pat.cnpj}):
        raise HTTPException(status_code=400, detail="Patrocinador já cadastrado")
    collection_patrocinadores.insert_one(pat.dict())
    return {"msg": f"Patrocinador {pat.nome} adicionado!"}



@app.post("/cancelar")
def cancelar_inscricao(cancelar: CancelarIn):
    part_doc = collection_participantes.find_one({"cpf": cancelar.cpf_participante})
    event_doc = collection_eventos.find_one({"nome": cancelar.nome_evento})

    if not part_doc or "evento" not in part_doc or cancelar.nome_evento not in part_doc["evento"]:
        raise HTTPException(status_code=404, detail="Participante não inscrito nesse evento")
    if not event_doc:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    collection_participantes.update_one(
        {"cpf": cancelar.cpf_participante},
        {"$pull": {"evento": cancelar.nome_evento}}
    )
    collection_eventos.update_one(
        {"nome": cancelar.nome_evento},
        {"$inc": {"participantes": -1}}
    )
    return {"msg": f"Inscrição de {part_doc['nome']} no evento {cancelar.nome_evento} cancelada!"}


@app.patch("/eventos/{id_evento}")
def atualizar_evento(
    id_evento: int = Path(..., description="ID do evento a ser atualizado"),
    atualizacao: AtualizarEventoIn = None
):
    evento_doc = collection_eventos.find_one({"id": id_evento})
    if not evento_doc:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    update_dict = {}

    # Adicionar palestrantes
    if atualizacao.cpfs_palestrantes:
        nomes_palestrantes = []
        for cpf in atualizacao.cpfs_palestrantes:
            pal_doc = collection_palestrantes.find_one({"cpf": cpf})
            if not pal_doc:
                raise HTTPException(status_code=404, detail=f"Palestrante com CPF {cpf} não encontrado")
            nomes_palestrantes.append(pal_doc["nome"])
        if nomes_palestrantes:
            update_dict["palestrantes"] = {"$each": nomes_palestrantes}

    # Adicionar patrocinadores
    if atualizacao.cnpjs_patrocinadores:
        nomes_patrocinadores = []
        for cnpj in atualizacao.cnpjs_patrocinadores:
            pat_doc = collection_patrocinadores.find_one({"cnpj": cnpj})
            if not pat_doc:
                raise HTTPException(status_code=404, detail=f"Patrocinador com CNPJ {cnpj} não encontrado")
            nomes_patrocinadores.append(pat_doc["nome"])
        if nomes_patrocinadores:
            update_dict["patrocinadores"] = {"$each": nomes_patrocinadores}

    if update_dict:
        # Usar $addToSet para evitar duplicatas
        update_query = {}
        if "palestrantes" in update_dict:
            update_query["palestrantes"] = {"$each": update_dict["palestrantes"]["$each"]}
        if "patrocinadores" in update_dict:
            update_query["patrocinadores"] = {"$each": update_dict["patrocinadores"]["$each"]}

        collection_eventos.update_one(
            {"id": id_evento},
            {"$addToSet": update_query}
        )

    return {"msg": f"Evento {evento_doc['nome']} atualizado com sucesso!"}