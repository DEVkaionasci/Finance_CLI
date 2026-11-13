from finance.models.conta import ContaCorrente
from finance.services.autenticacao import gerar_senha, verificar_senha
from finance.services.persistencia import *
from colorama import Fore
from stdiomask import getpass
from decimal import Decimal, InvalidOperation
import json

# DEIXA O TEXTO VERDE
print(Fore.GREEN)

contas = carregar_contas()
conta_ativa = None

# PRIMEIRO ACESSO
print("1 - ENTRAR\n2 - CADASTRAR")
opcao_acesso = input(">>")

# JÁ POSSUI CONTA
if opcao_acesso == '1':
    nome_conta = input("NOME DO TITULAR: ")

    conta_encontrada = None

    for conta in contas:
        if conta.titular == nome_conta:
            conta_encontrada = conta
            break

    if conta_encontrada is None:
        print("CONTA NÃO ENCONTRADA")
    else:
        print("SENHA")
        senha = getpass(">> ", mask="*")

        resultado = verificar_senha(
            senha,
            conta_encontrada._salt,
            conta_encontrada._hash_senha
        )

        if resultado:
            print("LOGIN REALIZADO COM SUCESSO!")
            conta_ativa = conta_encontrada
        else:
            print("SENHA INCORRETA")

# NÃO POSSUI CONTA OU DESEJA CRIAR OUTRA
elif opcao_acesso == '2':
    nome = input("SEU NOME COMPLETO: ")
    senha = getpass("SUA SENHA: ", mask='*')

    salt, hash_senha = gerar_senha(senha)

    nova_conta = ContaCorrente(
        nome,
        salt=salt,
        hash_senha=hash_senha
    )
    contas.append(nova_conta)
    salvar_contas(contas)

    if nova_conta:
        print("CONTA CRIADA COM SUCESSO!")
        conta_ativa = nova_conta
    else:
        print("ERRO AO CRIAR CONTA!")

if conta_ativa is not None:
    opcao = -1
    while opcao != '0':

        print("======POOBANK=====")
        print("1 - SALDO")
        print("2 - SACAR")
        print("3 - DEPOSITAR")
        print("4 - TRANSAÇÕES")
        print("0 - SAIR")
        print("===================")
        opcao = input(">>")

        match opcao:
            case '1':
                print(conta_ativa)

            case '2':
                valor = Decimal(input("VALOR PARA SAQUE: "))
                if conta_ativa.sacar(valor):
                    print(f"R${valor:.2f} SACADO COM SUCESSO!")
                    salvar_contas(contas)
                else:
                    print("FALHA NA TRANSAÇÃO")

            case '3':
                while True:
                    try:
                        valor = Decimal(input("VALOR PARA DEPÓSITO: "))
                        break
                    except InvalidOperation:
                        print("VALOR INVÁLIDO!")

                if conta_ativa.depositar(valor):
                    print(f"R${valor:.2f} DEPOSITADO COM SUCESSO!")
                    salvar_contas(contas)
                else:
                    print("FALHA NA TRANSAÇÃO")

            case '4':
                conta_ativa.exibir_historico()