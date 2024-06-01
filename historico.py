from transacao import Deposito, Saque

class Historico:
    
    def __init__(self, numero:int):
        self._numero = numero
        self._historico = str

    def adicionar_transacao(self, transacao):
        if transacao[0] == "s":
            Saque().registrar(self._numero, transacao[1])
        elif transacao[0] == "d":
            Deposito().registrar(self._numero, transacao[1])
        else:
            return False
        return True

    @property
    def historico(self):
        with open(f'./dados/conta-{self._numero}.txt', 'r') as file:
            for line in file.readlines():
                print(f"{line:<10}{'-' * 30}")
        return True