from database import connect

def criar_evento(nome, data, cpf_organizador):
    db = connect()
    evento = {"nome": nome, "data": data, "organizador": cpf_organizador}
    db.eventos.insert_one(evento)
    return evento

def listar_eventos():
    db = connect()
    return list(db.eventos.find({}, {"_id": 0}))