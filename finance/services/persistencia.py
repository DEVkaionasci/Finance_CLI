from finance.models.conta import ContaCorrente
from finance.models.transacao import Transacao
import datetime
from decimal import Decimal
import json

def salvar_contas(contas):

    dados = []

    for conta in contas:

        transacoes = []
        
        for transacao in conta._transacoes:
            dados_transacao = {
                "tipo": transacao.tipo,
                "valor": str(transacao.valor),
                "data_horario": transacao.data_horario.isoformat()
            }
        
            transacoes.append(dados_transacao)

        dados_conta = {
            "titular": conta.titular,
            "salt": conta._salt.hex(),
            "hash_senha": conta._hash_senha.hex(),
            "saldo": str(conta.saldo),
            "limite_credito": str(conta.limite_credito),
            "credito_utilizado": str(conta.credito_utilizado),
            "transacoes": transacoes
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
        salt = bytes.fromhex(conta["salt"])
        hash_senha = bytes.fromhex(conta["hash_senha"])

        nova_conta = ContaCorrente(
            conta["titular"],
            saldo=Decimal(conta["saldo"]),
            salt=salt,
            hash_senha=hash_senha,
            limite_credito=Decimal(conta["limite_credito"])
        )

        nova_conta._credito_utilizado = Decimal(conta["credito_utilizado"])
        for dados_transacao in conta.get("transacoes", []):
            transacao = Transacao(
                tipo=dados_transacao["tipo"],
                valor=Decimal(dados_transacao["valor"]),
                data_horario=datetime.datetime.fromisoformat(
                    dados_transacao["data_horario"]
                )
            )

            nova_conta.registrar_transacao(transacao)
            
        contas.append(nova_conta)

    return contas