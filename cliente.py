from conta import Conta, ContaCorrente
from datetime import date
import json
import re

ESTADOS = {
    "Acre": "AC",
    "Alagoas": "AL",
    "Amapá": "AP",
    "Amazonas": "AM",
    "Bahia": "BA",
    "Ceará": "CE",
    "Espírito Santo": "ES",
    "Goiás": "GO",
    "Maranhão": "MA",
    "Mato Grosso": "MT",
    "Mato Grosso do Sul": "MS",
    "Minas Gerais": "MG",
    "Pará": "PA",
    "Paraíba": "PB",
    "Paraná": "PR",
    "Pernambuco": "PE",
    "Piauí": "PI",
    "Rio de Janeiro": "RJ",
    "Rio Grande do Norte": "RN",
    "Rio Grande do Sul": "RS",
    "Rondônia": "RO",
    "Roraima": "RR",
    "Santa Catarina": "SC",
    "São Paulo": "SP",
    "Sergipe": "SE",
    "Tocantins": "TO",
}


class PessoaFisica:
    def __new__(cls, cpf, nome, data_nasc):
        try:
            data = cls.validar_data_nasc(cls, data_nasc)
            cpf_none = cls.validar_cpf(cls, cpf)
            if data == "Menor de idade":
                raise TypeError("Não foi possível criar a conta.")
            elif cpf_none is None:
                raise Exception("Não foi possível criar a conta.")
            else:
                return super(PessoaFisica, cls).__new__(cls)
        except Exception as err:
            print(f"\n{err}")
            return None
        
    
    def __init__(self, cpf: str, nome: str, data_nasc: date):
        self._cpf = cpf
        self._nome = nome
        self._data_nasc = self.validar_data_nasc(data_nasc)

    @property
    def nome(self):
        return self._nome

    @property
    def cpf(self):
        return self._cpf

    @property
    def data_nasc(self):
        return self._data_nasc.strftime('%d-%m-%Y')

    def validar_cpf(self, cpf):
        regex = re.compile(r'\d{11}').search(cpf)
        if regex:
            return cpf
        print("\nO CPF deve conter 11 números.\n")
        return None

    def validar_data_nasc(self, data_nasc):
        data_atual = date.today()
        try:
            validacao = data_nasc.split("/") if data_nasc.find("/") != -1 else data_nasc.split("-")
            data = date.fromisoformat(f"{validacao[2]}-{validacao[1]}-{validacao[0]}")
            diferenca_datas = (data_atual - data) / 365.25
            idade = diferenca_datas.days
            if idade < 18:
                print("\nPara abrir uma conta você deve ser maior de 18 anos de idade!\n")
                return "Menor de idade"
        except ValueError:
            print("""
                \rData inválida!
                \rO formato deve ser "dd/mm/yyyy" ou "dd-mm-yyyy", onde:
                \r\tdd = dia (2 caracteres)
                \r\tmm = mês (2 caracteres)
                \r\tyyyy = ano (4 caracteres)
                \rDigite-a novamente: """, end="")
            data = input()
            validar_data_nasc(data)
        return data


class Cliente(PessoaFisica):
    def checar_clientes():
        with open('./dados/clientes.json', 'r') as file:
            clientes = json.load(file)
        return clientes

    def __init__(self, cpf, nome, data_nasc, contas: list=[]):
        super().__init__(cpf, nome, data_nasc)
        clientes = Cliente.checar_clientes()
        novo_cliente = clientes.get(cpf, None)
        self._endereco = self.definir_endereco() if novo_cliente is None else clientes[cpf]["endereco"]
        self._contas = contas if novo_cliente is None else clientes[cpf]["contas"]
        if novo_cliente is None:
            with open('./dados/clientes.json', 'w') as file:
                clientes[cpf] = {}
                clientes[cpf]["nome"] = self.nome
                clientes[cpf]["contas"] = self.contas
                clientes[cpf]["endereco"] = self.endereco
                clientes[cpf]["data_nasc"] = self.data_nasc
                file.write(json.dumps(clientes))
    
    def validar_endereco(self, endereco:dict):
        estado = endereco.get('estado', None)
        while estado.title() not in ESTADOS.keys() and estado.upper() not in ESTADOS.values():
            estado = input("O estado que você forneceu é inválido, digite novamente: ")
        if estado.title() in ESTADOS.keys():
            estado = estado.title()
            sigla = ESTADOS[estado.title()]
        elif estado.upper() in ESTADOS.values():
            sigla = estado.upper()
            for e, uf in ESTADOS.items():
                if sigla == uf:
                    estado = e.title()
        endereco["estado"] = estado
        endereco["sigla"] = sigla
        return endereco

    def definir_endereco(self):
        endereco = {}
        endereco["logradouro"] = input("Digite a rua/avenida da sua residência: ")
        endereco["numero_residencia"] = input("Digite o número da sua residência: ")
        endereco["bairro"] = input("Digite o bairro onde você reside: ")
        endereco["cidade"] = input("Digite a cidade onde você reside: ")
        endereco["estado"] = input("Digite o estado em que você reside: ")
        endereco = self.validar_endereco(endereco)
        return endereco

    @property
    def endereco(self):
        return f'{self._endereco["logradouro"].title()}, {self._endereco["numero_residencia"]} - {self._endereco["bairro"]}-{self._endereco["cidade"]}/{self._endereco["sigla"]} {self._endereco["estado"]}'

    @property
    def contas(self):
        return self._contas

    def adicionar_conta(self):
        with open('./dados/contas.json', 'r') as contas:
            contas = json.load(contas)

        tipo_de_conta = input("Qual o tipo de conta: Padrao(p) | Corrente(c): ")
        while tipo_de_conta not in "pc":
            tipo_de_conta = input("Tipo de conta inválido! Digite: Padrao(p) | Corrente(c): ")
        nova_conta = len(contas.keys()) + 1
        contas[str(nova_conta)] = {}
        if tipo_de_conta == "p":
            conta = Conta.nova_conta(self, numero=nova_conta)
        elif tipo_de_conta == "c":
            conta = ContaCorrente.nova_conta(self, numero=nova_conta, saldo=0, limite=float(input("Digite o limite para saque diário: ")), limite_saque=int(input("Digite a quantidade máxima de saques por dia: ")))
            contas[str(nova_conta)]["limite"] = conta._limite
            contas[str(nova_conta)]["limite_saque"] = conta._limite_saque
            contas[str(nova_conta)]["limite_padrao"] = conta._limite
            contas[str(nova_conta)]["limite_saque_padrao"] = conta._limite_saque
        self._contas.append(conta)
        contas[str(nova_conta)]["cliente"] = self.nome
        contas[str(nova_conta)]["cpf"] = self.cpf
        contas[str(nova_conta)]["saldo"] = conta.saldo
        contas = json.dumps(contas)
        
        with open('./dados/contas.json', 'w') as novo:
            novo.write(contas)
        clientes = Cliente.checar_clientes()
        clientes[self.cpf]["contas"].append(nova_conta)
        with open('./dados/clientes.json', 'w') as file:
            file.write(json.dumps(clientes))
        return True
