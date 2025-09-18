# models.py
class Organizador:
    def __init__(self, nome: str, telefone: str, cpf: str):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf

class Participante:
    def __init__(self, nome: str, telefone: str, cpf: str, curso: str):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.curso = curso


class Evento:
    _id_counter = 1  # valor default, será atualizado antes de criar instâncias

    def __init__(self, nome: str, data: str, local: str, descricao: str, organizador):
        self.id = Evento._id_counter
        Evento._id_counter += 1
        self.nome = nome
        self.data = data
        self.local = local
        self.descricao = descricao
        self.organizador = organizador
        self.participantes = []

    def add_participante(self, participante: Participante):
        self.participantes.append(participante)

    def calcula_participantes(self):
        return len(self.participantes)

class Palestrante:
    def __init__(self, nome: str, telefone: str, cpf: str):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf

class Patrocinador:
    def __init__(self, nome: str, telefone: str, cnpj: str, valor_investido: float):
        self.nome = nome
        self.telefone = telefone
        self.cnpj = cnpj
        self.valor_investido = valor_investido
