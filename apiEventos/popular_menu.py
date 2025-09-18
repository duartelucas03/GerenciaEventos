from models import Participante, Evento, Organizador, Palestrante, Patrocinador
from database import (
    collection_participantes,
    collection_eventos,
    collection_organizadores,
    collection_palestrantes,
    collection_patrocinadores,
)
from pymongo import UpdateOne

def listar_colecao(nome_colecao, collection, campos=None):
    print(f"\n--- {nome_colecao} ---")
    docs = list(collection.find({}))
    if not docs:
        print("Nenhum registro encontrado.")
        return
    for doc in docs:
        if campos:
            print(", ".join(f"{campo}: {doc.get(campo, '')}" for campo in campos))
        else:
            print(doc)
    print("--------------------\n")

def menu_popular_banco():
    print("=== Menu de Gerenciamento do Banco ===")

    while True:
        print("\nEscolha uma opção:")
        print("2 - Adicionar organizador")
        print("3 - Adicionar participante")
        print("4 - Adicionar evento")
        print("5 - Inscrever participante em evento")
        print("6 - Adicionar palestrante")
        print("7 - Adicionar patrocinador")
        print("8 - Listar coleções")
        print("9 - Cancelar inscrição de participante em evento")
        print("0 - Sair")

        opcao = input("Opção: ").strip()

        if opcao == "0":
            break

        elif opcao == "2":
            nome = input("Nome do organizador: ")
            telefone = input("Telefone: ")
            cpf = input("CPF: ")
            org = Organizador(nome, telefone, cpf)
            collection_organizadores.insert_one({"nome": org.nome, "telefone": org.telefone, "cpf": org.cpf})
            print(f"Organizador {nome} adicionado!")

        elif opcao == "3":
            nome = input("Nome do participante: ")
            telefone = input("Telefone: ")
            cpf = input("CPF: ")
            curso = input("Curso: ")
            participante = Participante(nome, telefone, cpf, curso)
            collection_participantes.update_one(
                {"cpf": cpf},
                {"$setOnInsert": {"nome": nome, "telefone": telefone, "cpf": cpf, "curso": curso}},
                upsert=True
            )
            print(f"Participante {nome} cadastrado!")

        elif opcao == "4":
            listar_colecao("Organizadores", collection_organizadores, campos=["nome", "cpf"])
            nome = input("Nome do evento: ")
            data = input("Data (dd-mm-aaaa): ")
            local = input("Local: ")
            descricao = input("Descrição: ")
            cpf_org = input("CPF do organizador: ")

            org_doc = collection_organizadores.find_one({"cpf": cpf_org})
            if not org_doc:
                print("Organizador não encontrado! Cadastre primeiro.")
                continue

            ultimo = collection_eventos.find_one(sort=[("id", -1)], projection={"id": 1, "_id": 0})
            proximo_id = ultimo["id"] + 1 if ultimo else 1

            org = Organizador(org_doc["nome"], org_doc["telefone"], org_doc["cpf"])

            # Selecionar palestrantes
            listar_colecao("Palestrantes", collection_palestrantes, campos=["nome", "cpf"])
            cpfs_palestrantes = input("Digite os CPFs dos palestrantes separados por vírgula (ou deixe vazio): ")
            palestrantes_evento = []
            if cpfs_palestrantes:
                for cpf in cpfs_palestrantes.split(","):
                    cpf = cpf.strip()
                    pal_doc = collection_palestrantes.find_one({"cpf": cpf})
                    if pal_doc:
                        palestrantes_evento.append(pal_doc["nome"])

            # Selecionar patrocinadores
            listar_colecao("Patrocinadores", collection_patrocinadores, campos=["nome", "cnpj"])
            cnpjs_patrocinadores = input("Digite os CNPJs dos patrocinadores separados por vírgula (ou deixe vazio): ")
            patrocinadores_evento = []
            if cnpjs_patrocinadores:
                for cnpj in cnpjs_patrocinadores.split(","):
                    pat_doc = collection_patrocinadores.find_one({"cnpj": cnpj.strip()})
                    if pat_doc:
                        patrocinadores_evento.append(pat_doc["nome"])

            evento = Evento(nome, data, local, descricao, org)
            evento.id = proximo_id

            collection_eventos.insert_one({
                "id": evento.id,
                "nome": evento.nome,
                "data": evento.data,
                "local": evento.local,
                "descricao": evento.descricao,
                "participantes": evento.calcula_participantes(),
                "organizador": evento.organizador.nome,
                "palestrantes": palestrantes_evento,
                "patrocinadores": patrocinadores_evento
            })
            print(f"Evento {nome} adicionado!")


        elif opcao == "5":
            listar_colecao("Participantes", collection_participantes, campos=["nome", "cpf"])
            listar_colecao("Eventos", collection_eventos, campos=["nome", "id"])
            cpf_part = input("CPF do participante: ")
            id_evento = int(input("Id do evento: "))  # <-- converter para inteiro

            part_doc = collection_participantes.find_one({"cpf": cpf_part})
            event_doc = collection_eventos.find_one({"id": id_evento})

            if not part_doc:
                print("Participante não encontrado!")
                continue
            if not event_doc:
                print("Evento não encontrado!")
                continue

            nome_evento = event_doc["nome"]

            # Adiciona evento ao participante
            collection_participantes.update_one(
                {"cpf": cpf_part},
                {"$addToSet": {"evento": nome_evento}}
            )

            # Atualiza contador de participantes no evento
            novos_total = event_doc.get("participantes", 0) + 1
            collection_eventos.update_one(
                {"id": id_evento},  # <-- usar id na busca
                {"$set": {"participantes": novos_total}}
            )

            print(f"Participante {part_doc['nome']} inscrito no evento {nome_evento}!")

        elif opcao == "6":
            nome = input("Nome do palestrante: ")
            telefone = input("Telefone: ")
            cpf = input("CPF: ")
            palestrante = Palestrante(nome, telefone, cpf)
            collection_palestrantes.insert_one({"nome": palestrante.nome, "telefone": palestrante.telefone, "cpf": palestrante.cpf})
            print(f"Palestrante {nome} adicionado!")

        elif opcao == "7":
            nome = input("Nome do patrocinador: ")
            telefone = input("Telefone: ")
            cnpj = input("CNPJ: ")
            valor = float(input("Valor investido: "))
            pat = Patrocinador(nome, telefone, cnpj, valor)
            collection_patrocinadores.insert_one({"nome": pat.nome, "telefone": pat.telefone, "cnpj": pat.cnpj, "valorInvestido": pat.valor_investido})
            print(f"Patrocinador {nome} adicionado!")

        elif opcao == "8":
            listar_colecao("Organizadores", collection_organizadores, campos=["nome", "cpf"])
            listar_colecao("Participantes", collection_participantes, campos=["nome", "cpf", "curso"])
            listar_colecao("Eventos", collection_eventos, campos=["nome", "id", "participantes"])
            listar_colecao("Palestrantes", collection_palestrantes, campos=["nome", "cpf"])
            listar_colecao("Patrocinadores", collection_patrocinadores, campos=["nome", "cnpj", "valorInvestido"])

        elif opcao == "9":
                    listar_colecao("Participantes", collection_participantes, campos=["nome", "cpf", "evento"])
                    listar_colecao("Eventos", collection_eventos, campos=["nome", "participantes"])
                    cpf_part = input("CPF do participante: ")
                    nome_evento = input("Nome do evento: ")

                    part_doc = collection_participantes.find_one({"cpf": cpf_part})
                    event_doc = collection_eventos.find_one({"nome": nome_evento})

                    if not part_doc:
                        print("Participante não encontrado!")
                        continue
                    if not event_doc:
                        print("Evento não encontrado!")
                        continue
                    if "evento" not in part_doc or nome_evento not in part_doc.get("evento", []):
                        print("Participante não está inscrito nesse evento!")
                        continue

                    # Remove evento do participante
                    collection_participantes.update_one(
                        {"cpf": cpf_part},
                        {"$pull": {"evento": nome_evento}}
                    )

                    # Atualiza contador de participantes no evento
                    novos_total = max(event_doc.get("participantes", 1) - 1, 0)
                    collection_eventos.update_one(
                        {"nome": nome_evento},
                        {"$set": {"participantes": novos_total}}
                    )

                    print(f"Inscrição de {part_doc['nome']} no evento {nome_evento} cancelada!")

        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    menu_popular_banco()
