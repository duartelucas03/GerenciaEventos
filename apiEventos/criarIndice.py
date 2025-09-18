from database import collection_participantes
from database import collection_palestrantes
from database import collection_organizadores
from database import collection_patrocinadores
from database import collection_eventos

# Criar índice para o campo "cpf"
collection_participantes.create_index("cpf", unique=True)
print("Índice criado para o campo 'cpf' dos participantes")


collection_palestrantes.create_index("cpf", unique=True)
print("Índice criado para o campo 'cpf' dos palestrantes")


collection_organizadores.create_index("cpf", unique=True)
print("Índice criado para o campo 'cpf' dos organizadores")

collection_patrocinadores.create_index("cnpj", unique=True)
print("Índice criado para o campo 'cnpj' dos patrocinadores")

collection_eventos.create_index("id", unique=True)
print("Índice criado para o campo 'id' dos eventos")