from abc import ABC, abstractmethod


class Transacao(ABC):
    
    @abstractmethod
    def registrar(self):
        pass


class Deposito(Transacao):
    def registrar(self, conta, valor):
        with open(f'./dados/conta-{conta}.txt', 'a') as file:
            file.write(f"Deposito: R$ {valor:.2f}\n")
        return True


class Saque(Transacao):
    def registrar(self, conta, valor):
        with open(f'./dados/conta-{conta}.txt', 'a') as file:
            file.write(f"Saque: R$ {valor:.2f}\n")
        return True
