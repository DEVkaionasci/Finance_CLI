from finance.models.conta import ContaCorrente
from decimal import Decimal
import json

def salvar_contas(contas):
    dados = []

    for conta in contas:
        dados_conta = {
            "titular": conta.titular,
            "saldo": str(conta.saldo),
            "limite_credito": str(conta.limite_credito),
            "credito_utilizado": str(conta.credito_utilizado)
        }

        dados.append(dados_conta)

    with open("contas.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


def carregar_contas():
    try:
        with open("contas.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    contas = []

    for conta in dados:
         nova_conta = ContaCorrente(
              conta["titular"],
              saldo=Decimal(conta["saldo"]),
              limite_credito=Decimal(conta["limite_credito"])
         )

         nova_conta._credito_utilizado = Decimal(conta["credito_utilizado"])
         contas.append(nova_conta)

    return contas