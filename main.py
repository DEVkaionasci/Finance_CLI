from finance.models.conta import ContaCorrente
from finance.services.persistencia import *
from colorama import Fore
from stdiomask import getpass
from decimal import Decimal, InvalidOperation
import json

#MAKE THE TEXT GREEN
print(Fore.GREEN)

contas = carregar_contas()
#FIRST LOGIN
print("1 - LOGIN\n2 - SIGN UP")
new_or_not = input(">>")

#ALREADY HAS AN ACCOUNT
if(new_or_not == '1'):
    pass
#DONT HAVE ONE YET OR CREATE ANOTHER
else:
    nome = input("YOUR FULL NAME: ")
    senha = getpass("YOUR PASSWORD: ", mask='*')
    nova_conta = ContaCorrente(nome, senha=senha)
    contas = [nova_conta]

    salvar_contas(contas)

    if (nova_conta):
        print("ACCOUNT CREATED WITH SUCESS!")
    else:
        print("ERROR CREATING ACCOUNT!")

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
            print(nova_conta)

        case '2':
            valor = Decimal(input("VALUE TO WITHDRAWN: "))
            if nova_conta.sacar(valor):
                print(f"R${valor:.2f} WITHDRAWED WITH SUCESS!")
            else:
                print("TRANSACTION FAILURE")

        case '3':
            while True:
                try:
                    valor = Decimal(input("VALUE TO DEPOSIT: "))
                    break
                except InvalidOperation:
                    print("INVALID VALUE!")

            if(nova_conta.depositar(valor)):
                print(f"R${valor:.2f} DEPOSITED WITH SUCESS!")
            else:
                print("TRANSACTION FAILURE")

        case '4':
            nova_conta.exibir_historico()