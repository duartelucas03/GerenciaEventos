from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pymongo import MongoClient
import os
from datetime import datetime
from database import (
    collection_participantes,
    collection_eventos,
)


def gerar_certificados(nome_evento):
    # Busca o evento
    evento = collection_eventos.find_one({"nome": nome_evento})
    if not evento:
        print(f"Evento '{nome_evento}' não encontrado!")
        return

    participantes = collection_participantes.find({"evento": nome_evento})

    pasta_certificados = f"certificados_{nome_evento.replace(' ', '_')}"
    os.makedirs(pasta_certificados, exist_ok=True)

    for part in participantes:
        nome = part.get("nome")
        cpf = part.get("cpf")
        data_evento = evento.get("data")

        # Nome do arquivo PDF
        arquivo_pdf = os.path.join(pasta_certificados, f"{nome.replace(' ', '_')}.pdf")
        c = canvas.Canvas(arquivo_pdf, pagesize=A4)
        largura, altura = A4

        # Texto centralizado
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(largura / 2, altura - 150, "CERTIFICADO DE PARTICIPAÇÃO")

        c.setFont("Helvetica", 16)
        c.drawCentredString(largura / 2, altura - 220, f"Certificamos que {nome} (CPF: {cpf})")
        c.drawCentredString(largura / 2, altura - 250, f"participou do evento '{nome_evento}'")
        c.drawCentredString(largura / 2, altura - 280, f"realizado em {data_evento}")

        # Assinatura fictícia
        c.drawString(100, 100, f"__________________________")
        c.drawString(100, 80, f"Organizador: {evento.get('organizador', '---')}")

        c.save()
        print(f"Certificado gerado para {nome}!")

if __name__ == "__main__":
    nome_evento = input("Digite o nome do evento para gerar os certificados: ")
    gerar_certificados(nome_evento)
