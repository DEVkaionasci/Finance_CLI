from finance.models.conta import ContaCorrente
from finance.services.autenticacao import gerar_senha, verificar_senha
from finance.services.persistencia import *
from colorama import Fore
from stdiomask import getpass
from decimal import Decimal, InvalidOperation
import json

#MAKE THE TEXT GREEN
print(Fore.GREEN)

contas = carregar_contas()
conta_ativa = None

#FIRST LOGIN
print("1 - LOGIN\n2 - SIGN UP")
new_or_not = input(">>")

#ALREADY HAS AN ACCOUNT
if(new_or_not == '1'):
    account_name = input("NAME OF ACCOUNT: ")

    found_account = None

    for conta in contas:
        if conta.titular == account_name:
            found_account = conta
            break

    if found_account is None:
        print("ACCOUNT NOT FOUND")
    else:
        print("PASSWORD")
        password = input(">> ")

        resultado = verificar_senha(password, 
                        found_account._salt,
                        found_account._hash_senha
                        )

        if resultado:
            print("LOGIN SUCESSFUL")
            conta_ativa = found_account
        else:
            print("INCORRECT PASSWORD")

#DONT HAVE ONE YET OR CREATE ANOTHER
else:
    nome = input("YOUR FULL NAME: ")
    senha = getpass("YOUR PASSWORD: ", mask='*')

    salt, hash_senha = gerar_senha(senha)

    nova_conta = ContaCorrente(
        nome,
        salt=salt,
        hash_senha=hash_senha
    )
    contas.append(nova_conta)
    salvar_contas(contas)

    if (nova_conta):
        print("ACCOUNT CREATED WITH SUCESS!")
        conta_ativa = nova_conta
    else:
        print("ERROR CREATING ACCOUNT!")

if conta_ativa is not None:
    opcao = -1
    while(opcao != '0'):

        print("======POOBANK=====")
        print("1 - BALANCE")
        print("2 - WITHDRAW")
        print("3 - DEPOSIT")
        print("4 - TRANSACTIONS")
        print("0 - EXIT")
        print("===================")
        opcao = input(">>")

        match opcao:
            case '1':
                print(conta_ativa)

            case '2':
                valor = Decimal(input("VALUE TO WITHDRAWN: "))
                if conta_ativa.sacar(valor):
                    print(f"R${valor:.2f} WITHDRAWED WITH SUCESS!")
                    salvar_contas(contas)
                else:
                    print("TRANSACTION FAILURE")

            case '3':
                while True:
                    try:
                        valor = Decimal(input("VALUE TO DEPOSIT: "))
                        break
                    except InvalidOperation:
                        print("INVALID VALUE!")

                if(conta_ativa.depositar(valor)):
                    print(f"R${valor:.2f} DEPOSITED WITH SUCESS!")
                    salvar_contas(contas)
                else:
                    print("TRANSACTION FAILURE")

            case '4':
                conta_ativa.exibir_historico()