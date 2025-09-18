# inscrever_participantes_aleatorio.py
from database import collection_participantes, collection_eventos
from pymongo import UpdateOne
import random

def inscrever_participantes_aleatoriamente():
    participantes = list(collection_participantes.find({}))
    eventos = list(collection_eventos.find({}))

    if not participantes or not eventos:
        print("Não há participantes ou eventos cadastrados.")
        return

    operations_eventos = []
    operations_participantes = []

    for participante in participantes:
        # Escolhe aleatoriamente 1 ou 2 eventos
        eventos_aleatorios = random.sample(eventos, k=random.randint(1, min(2, len(eventos))))

        for evento in eventos_aleatorios:
            # Atualiza participante para incluir o evento
            operations_participantes.append(
                UpdateOne(
                    {"cpf": participante["cpf"]},
                    {"$addToSet": {"evento": evento["nome"]}}
                )
            )

            # Atualiza apenas o contador de participantes do evento (sem adicionar nomes)
            operations_eventos.append(
                UpdateOne(
                    {"id": evento["id"]},
                    {"$inc": {"participantes": 1}}
                )
            )

    if operations_participantes:
        collection_participantes.bulk_write(operations_participantes)
    if operations_eventos:
        collection_eventos.bulk_write(operations_eventos)

    print(f"{len(participantes)} participantes inscritos aleatoriamente em eventos existentes.")

if __name__ == "__main__":
    inscrever_participantes_aleatoriamente()
