from historico import Historico


class Conta:

    def __init__(self, cliente, numero: int, saldo: float, agencia: str="0001", historico: Historico=None):
        self._agencia = agencia
        self._numero = numero
        self._saldo = saldo
        self._cliente = cliente
        self._historico = historico

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero
    
    @property
    def historico(self):
        return self._historico.historico

    @classmethod
    def nova_conta(cls, cliente, numero: int, saldo: float=0):
        return cls(cliente, numero, saldo)
    
    def sacar(self, valor: float):
        if valor <= self._saldo:
            self._saldo -= valor
            if self._historico is None:
                self._historico = Historico(self._numero)
            self._historico.adicionar_transacao(("s", valor))
            return True
        return False
    
    def depositar(self, valor: float):
        if valor > 0:
            self._saldo += valor
            if self._historico is None:
                self._historico = Historico(self._numero)
            self._historico.adicionar_transacao(("d", valor))
            return True
        return False


class ContaCorrente(Conta):
    
    def __init__(self, cliente, numero, saldo, limite: float, limite_saque: int):
        super().__init__(cliente, numero, saldo)
        self._limite = limite
        self._limite_saque = limite_saque
    
    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saque(self):
        return self._limite_saque

    @classmethod
    def nova_conta(cls, cliente, numero: int, saldo: float, limite: float, limite_saque: int):
        return cls(cliente, numero, saldo, limite, limite_saque)

    def sacar(self, valor: float):
        if self._limite_saque != 0 and valor <= self._limite and valor <= self._saldo:
            self._limite_saque -= 1
            self._limite -= valor
            self._saldo -= valor
            if self._historico is None:
                self._historico = Historico(self._numero)
            self._historico.adicionar_transacao(("s", valor))
            return True
        return False
