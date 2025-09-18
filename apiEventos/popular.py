# popular_banco_ficticio.py
from models import Participante, Evento, Organizador, Palestrante, Patrocinador
from database import (
    collection_participantes,
    collection_eventos,
    collection_organizadores,
    collection_palestrantes,
    collection_patrocinadores,
)

# Limpar coleções antes de popular
collection_participantes.delete_many({})
collection_eventos.delete_many({})
collection_organizadores.delete_many({})
collection_palestrantes.delete_many({})
collection_patrocinadores.delete_many({})

print("Coleções limpas. Iniciando população com dados fictícios...\n")

# ---------- Organizadores ----------
organizadores_ficticios = [
    {"nome": "Ana Silva", "telefone": "11988887777", "cpf": "11111111111"},
    {"nome": "Bruno Costa", "telefone": "11977778888", "cpf": "22222222222"},
    {"nome": "Carla Souza", "telefone": "11966669999", "cpf": "33333333333"},
    {"nome": "Diego Ramos", "telefone": "11955556666", "cpf": "44444444444"},
    {"nome": "Elisa Ferreira", "telefone": "11944445555", "cpf": "55555555555"},
]

for org in organizadores_ficticios:
    collection_organizadores.insert_one(org)
print("Organizadores adicionados.")

# ---------- Participantes ----------
participantes_ficticios = [
    {"nome": "Lucas Soares", "telefone": "11955554444", "cpf": "44444444444", "curso": "Gestão da Informação"},
    {"nome": "Mariana Lima", "telefone": "11944443333", "cpf": "55555555555", "curso": "Engenharia"},
    {"nome": "Pedro Santos", "telefone": "11933332222", "cpf": "66666666666", "curso": "Administração"},
    {"nome": "Fernanda Costa", "telefone": "11922221111", "cpf": "77777777777", "curso": "Direito"},
    {"nome": "Gabriel Almeida", "telefone": "11911110000", "cpf": "88888888888", "curso": "Medicina"},
    {"nome": "Isabela Rocha", "telefone": "11900009999", "cpf": "99999999999", "curso": "Arquitetura"},
    {"nome": "João Pedro", "telefone": "11888887777", "cpf": "10101010101", "curso": "Engenharia de Software"},
    {"nome": "Camila Nunes", "telefone": "11877776666", "cpf": "12121212121", "curso": "Ciência da Computação"},
    {"nome": "Rafael Lima", "telefone": "11866665555", "cpf": "13131313131", "curso": "Administração"},
    {"nome": "Juliana Martins", "telefone": "11855554444", "cpf": "14141414141", "curso": "Gestão da Informação"},
    {"nome": "Thiago Fernandes", "telefone": "11844443333", "cpf": "15151515151", "curso": "Engenharia"},
    {"nome": "Patrícia Souza", "telefone": "11833332222", "cpf": "16161616161", "curso": "Direito"},
    {"nome": "Vitor Henrique", "telefone": "11822221111", "cpf": "17171717171", "curso": "Medicina"},
    {"nome": "Beatriz Lima", "telefone": "11811110000", "cpf": "18181818181", "curso": "Arquitetura"},
    {"nome": "Felipe Rocha", "telefone": "11799998888", "cpf": "19191919191", "curso": "Engenharia de Software"},
    {"nome": "Larissa Nunes", "telefone": "11788887777", "cpf": "20202020202", "curso": "Ciência da Computação"},
    {"nome": "André Lima", "telefone": "11777776666", "cpf": "21212121212", "curso": "Administração"},
    {"nome": "Sabrina Martins", "telefone": "11766665555", "cpf": "22222222221", "curso": "Gestão da Informação"},
    {"nome": "Carlos Fernandes", "telefone": "11755554444", "cpf": "23232323232", "curso": "Engenharia"},
    {"nome": "Renata Souza", "telefone": "11744443333", "cpf": "24242424242", "curso": "Direito"},
    {"nome": "Lucas Almeida", "telefone": "11733332222", "cpf": "25252525252", "curso": "Medicina"},
    {"nome": "Amanda Rocha", "telefone": "11722221111", "cpf": "26262626262", "curso": "Arquitetura"},
    {"nome": "Daniel Lima", "telefone": "11711110000", "cpf": "27272727272", "curso": "Engenharia de Software"},
    {"nome": "Julio Nunes", "telefone": "11699998888", "cpf": "28282828282", "curso": "Ciência da Computação"},
    {"nome": "Fernanda Lima", "telefone": "11688887777", "cpf": "29292929292", "curso": "Administração"},
    {"nome": "Ricardo Martins", "telefone": "11677776666", "cpf": "30303030303", "curso": "Gestão da Informação"},
    {"nome": "Tatiane Fernandes", "telefone": "11666665555", "cpf": "31313131313", "curso": "Engenharia"},
    {"nome": "Paulo Souza", "telefone": "11655554444", "cpf": "32323232323", "curso": "Direito"},
    {"nome": "Michele Almeida", "telefone": "11644443333", "cpf": "33333333334", "curso": "Medicina"},
    {"nome": "Eduardo Rocha", "telefone": "11633332222", "cpf": "34343434343", "curso": "Arquitetura"},
]

for part in participantes_ficticios:
    collection_participantes.insert_one(part)
print("Participantes adicionados.")

# ---------- Palestrantes ----------
palestrantes_ficticios = [
    {"nome": "Dr. Ricardo Alves", "telefone": "11922221111", "cpf": "77777777777"},
    {"nome": "Profª. Helena Martins", "telefone": "11911110000", "cpf": "88888888888"},
    {"nome": "Dr. Felipe Santos", "telefone": "11999990000", "cpf": "89898989898"},
    {"nome": "Profª. Camila Lima", "telefone": "11988889999", "cpf": "90909090909"},
]

for pal in palestrantes_ficticios:
    collection_palestrantes.insert_one(pal)
print("Palestrantes adicionados.")

# ---------- Patrocinadores ----------
patrocinadores_ficticios = [
    {"nome": "TechCorp", "telefone": "1133334444", "cnpj": "12345678000199", "valorInvestido": 5000.0},
    {"nome": "InfoSolutions", "telefone": "1144445555", "cnpj": "98765432000188", "valorInvestido": 3000.0},
    {"nome": "DataMasters", "telefone": "1155556666", "cnpj": "11223344000177", "valorInvestido": 4000.0},
    {"nome": "SoftInnovate", "telefone": "1166667777", "cnpj": "99887766000155", "valorInvestido": 3500.0},
]

for pat in patrocinadores_ficticios:
    collection_patrocinadores.insert_one(pat)
print("Patrocinadores adicionados.")

# ---------- Eventos ----------
eventos_ficticios = [
    {
        "nome": "Semana de TI",
        "data": "10-09-2025",
        "local": "Auditório A",
        "descricao": "Evento sobre tendências em tecnologia da informação.",
        "limite": 50,
        "cpf_organizador": "11111111111",
        "cpfs_palestrantes": ["77777777777", "89898989898"],
        "cnpjs_patrocinadores": ["12345678000199", "11223344000177"]
    },
    {
        "nome": "Workshop de Gestão",
        "data": "15-09-2025",
        "local": "Sala 101",
        "descricao": "Oficinas práticas de gestão empresarial.",
        "limite": 30,
        "cpf_organizador": "22222222222",
        "cpfs_palestrantes": ["88888888888", "90909090909"],
        "cnpjs_patrocinadores": ["98765432000188", "99887766000155"]
    },
    {
        "nome": "Inovação e Startups",
        "data": "20-09-2025",
        "local": "Auditório B",
        "descricao": "Debates e apresentações sobre startups e inovação.",
        "limite": 40,
        "cpf_organizador": "33333333333",
        "cpfs_palestrantes": ["77777777777", "90909090909"],
        "cnpjs_patrocinadores": ["12345678000199", "99887766000155"]
    }
]

ultimo_id = 0
for evt in eventos_ficticios:
    org_doc = collection_organizadores.find_one({"cpf": evt["cpf_organizador"]})
    palestrantes_evento = [collection_palestrantes.find_one({"cpf": cpf})["nome"] for cpf in evt["cpfs_palestrantes"]]
    patrocinadores_evento = [collection_patrocinadores.find_one({"cnpj": cnpj})["nome"] for cnpj in evt["cnpjs_patrocinadores"]]

    ultimo_id += 1
    evento_doc = {
        "id": ultimo_id,
        "nome": evt["nome"],
        "data": evt["data"],
        "local": evt["local"],
        "descricao": evt["descricao"],
        "participantes": 0,
        "organizador": org_doc["nome"],
        "palestrantes": palestrantes_evento,
        "patrocinadores": patrocinadores_evento
    }
    collection_eventos.insert_one(evento_doc)
print("Eventos adicionados.")

print("\nBanco populado com sucesso!")
