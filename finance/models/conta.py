from abc import ABC, abstractmethod
from finance.models.transacao import Transacao


class Conta(ABC):
    def __init__(self, titular, saldo=0, salt=None, hash_senha=None):
        super().__init__()
        self._saldo = saldo             
        self._titular = titular
        self._salt = salt
        self._hash_senha = hash_senha
        self._transacoes = []


    def __str__(self):
        return f"Saldo atual da conta: R${self._saldo:.2f}"

    @property
    def saldo(self):
        return self._saldo   

    @property
    def titular(self):
        return self._titular

    @abstractmethod
    def sacar(self, valor):
        pass

    def depositar(self, valor):
        if valor > 0:
            transacao = Transacao("deposito", valor)
            if self.registrar_transacao(transacao):
                self._saldo += valor
                return True
        return False

    def registrar_transacao(self, transacao):
        self._transacoes.append(transacao)
        return True


    def exibir_historico(self):
        for transacao in self._transacoes:
            print(transacao)


class ContaCorrente(Conta):
    def __init__(self, titular, saldo=0, salt=None, hash_senha=None, limite_credito=500.0):
        super().__init__(titular, saldo, salt, hash_senha)
        self.limite_credito = limite_credito
        self._credito_utilizado = 0.0

    @property
    def credito_utilizado(self):
        return self._credito_utilizado

    @property
    def credito_disponivel(self):
        return self.limite_credito - self._credito_utilizado

    def sacar(self, valor):
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            transacao = Transacao("saque", valor)
            self.registrar_transacao(transacao)
            return True
        return False

    def sacar_credito(self, valor):
        if valor > 0 and valor <= self.credito_disponivel:
            self._credito_utilizado += valor
            transacao = Transacao("saque_credito", valor)
            self.registrar_transacao(transacao)
            return True
        return False

    def pagar_credito(self, valor):
        if (
            valor > 0
            and valor <= self._saldo
            and self._credito_utilizado > 0
            and valor <= self._credito_utilizado
        ):
            self._saldo -= valor
            self._credito_utilizado -= valor
            transacao = Transacao("pagamento_credito", valor)
            self.registrar_transacao(transacao)
            return True
        return False