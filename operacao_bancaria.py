from cliente import Cliente
from conta import Conta, ContaCorrente
from datetime import date
from os import system
import platform
import json

def abrir_sessao(mensagem=None):
    if platform.system() == "Windows":
        system("cls")
    else:
        system("clear")
    header = f"""
    {"=" * 30}
    {"sistema bancário dio".upper().center(30, " ")}
    {"=" * 30}

"""
    print(header)
    
    if mensagem is not None:
        print(f'\t{mensagem}')
    
def logar_cliente():
    cliente = input("Digite seu CPF para acessar sua conta: ")
    while len(cliente) != 11:
        cliente = input("CPF inválido. Tente novamente: ")
    clientes = Cliente.checar_clientes()
    if clientes.get(cliente, None) is None:
        return None

    return Cliente(cliente, clientes[cliente]["nome"], clientes[cliente]["data_nasc"])

def atualizar_dados_conta(contas, conta):
    contas[str(conta.numero)]["saldo"] = conta.saldo
    with open('./dados/contas.json', 'w') as file:
        file.write(json.dumps(contas))

hoje = date.today()
abrir_sessao()

while True:
    with open('./dados/clientes.json', 'r') as file:
        clientes = json.load(file)
    with open('./dados/contas.json', 'r') as file:
        contas = json.load(file)

    menu = """
    Qual operação deseja realizar?
    
    [1] Cadastrar cliente
    [2] Entrar com cliente
    [3] Cadastrar conta
    [4] Entrar com conta
    [5] Ver saldo
    [6] Depósito
    [7] Saque
    [8] Histórico
    [9] Sair
    """

    mensagem = None

    # ======================== DISPLAY MENU =============================
    print(menu)
    
    opcao = int(input("\tDigite sua opção desejada: "))

    # ======================= Opção inválida ============================
    if opcao not in range(1, 10):
        if platform.system() == "Windows":
            system("cls")
        else:
            system("clear")
        continue

    # ====================== Cadastrar cliente ==========================
    elif opcao == 1:
        cpf_novo_cliente = input("Digite seu CPF: ")
        cliente_cadastrado = clientes.get(cpf_novo_cliente, None)
        
        if cliente_cadastrado is None:
            nome_novo_cliente = input("Digite seu nome completo: ")
            nasc_novo_cliente = input("Digite sua data de nascimento: ")
            cliente = Cliente(cpf_novo_cliente, nome_novo_cliente, nasc_novo_cliente)
            if cliente:
                mensagem = " Cadastro realizado com sucesso! ".center(30, "=")
            else:
                break
        else:
            mensagem = " CPF já cadastrado! ".center(30, "=")

    #  ========================= Entrar cliente ==============================
    elif opcao == 2:
        cliente = logar_cliente()
        mensagem = " Entrada bem sucedida ".center(30, "=") if cliente is not None else "\r\tCliente não encontrado."
        
    #  ========================= Cadastrar conta ==============================
    elif opcao == 3:
        try:
            cliente.adicionar_conta()
        except NameError:
            cliente = logar_cliente()
            if cliente is not None:
                cliente.adicionar_conta()
                mensagem = " Conta adicionada. ".center(30, "=")
            else:
                mensagem = "\r\tCliente não cadastrado."

    # ======================= Entrar conta ===========================
    elif opcao == 4:
        cliente = logar_cliente()
        if cliente is None:
            mensagem = "\r\tCliente não cadastrado."
        else:
            contas_cliente = {}
            for numero_conta, dados in contas.items():
                if dados["cpf"] == cliente.cpf:
                    contas_cliente[numero_conta] = {}
                    contas_cliente[numero_conta]["saldo"] = dados["saldo"]
                    if dados.get('limite', None) is not None:
                        contas_cliente[numero_conta]["limite"] = dados["limite"]
                        contas_cliente[numero_conta]["limite_saque"] = dados["limite_saque"]
                        contas_cliente[numero_conta]["data_ultima_operacao"] = dados["data_ultima_operacao"]
                        contas_cliente[numero_conta]["limite_padrao"] = dados["limite_padrao"]
                        contas_cliente[numero_conta]["limite_saque_padrao"] = dados["limite_saque_padrao"]
                

            if len(contas_cliente.keys()) > 1:
                print("Qual número de conta deseja fazer operação?")
                for k in contas_cliente.keys():
                    print(k)
                conta = input()
                while conta not in contas_cliente.keys():
                    conta = input("Digite uma conta válida ou 's' para sair: ")
                    if conta.lower() == 's':
                        break
            elif len(contas_cliente.keys()) == 1:
                conta = str(cliente.contas[0])
            else:
                mensagem = "\r\tNão foi encontrada nenhuma conta com o CPF informado."

            if contas_cliente[conta].get('limite', None) is not None:
                ultima_operacao = date.fromisoformat(contas_cliente[conta]["data_ultima_operacao"])
                if ultima_operacao != hoje:
                    conta = ContaCorrente(cliente, int(conta), contas[conta]["saldo"], contas_cliente[conta]["limite_padrao"], contas_cliente[conta]["limite_saque_padrao"])
                else:
                    conta = ContaCorrente(cliente, int(conta), contas[conta]["saldo"], contas_cliente[conta]["limite"], contas_cliente[conta]["limite_saque"])
            else:
                conta = Conta(cliente, int(conta), contas[conta]["saldo"])

    # ====================== Ver Saldo ==========================
    
    elif opcao == 5:
        mensagem = f" Seu saldo é de R$ {conta.saldo:.2f} ".center(30, "=")

    # ====================== Opção de depósito ==========================
    elif opcao == 6:
        try:
            deposito = conta.depositar(int(input("Digite o valor a ser depositado: R$ ")))
            if not deposito:
                mensagem = "\r\tOperação não permitida."
            else:
                atualizar_dados_conta(contas, conta)
                mensagem = "\r\n" + " Operação bem sucedida. ".center(30, "=")
                mensagem += "\n" + f" Seu saldo é de R$ {conta.saldo:.2f} ".center(30, "=")
        except NameError:
            mensagem = "\r\tVocê precisa entrar com sua conta."

    #  ====================== Opção de saque ============================
    elif opcao == 7:
        try:
            valor = float(input("Digite o valor do saque: R$ "))
            saque = conta.sacar(valor)
            if not saque and hasattr(conta, "limite"):
                mensagem = "\tLimite excedido."
            elif saque and hasattr(conta, "limite"):
                contas[str(conta.numero)]["limite"] = conta.limite
                contas[str(conta.numero)]["limite_saque"] = conta.limite_saque
                contas[str(conta.numero)]["data_ultima_operacao"] = date.today().strftime("%d-%m-%Y")
                atualizar_dados_conta(contas, conta)
                mensagem = "\r\n" + " Operação bem sucedida. ".center(30, "=")
                mensagem += "\n" + f" Seu saldo é de R$ {conta.saldo:.2f} ".center(30, "=")
            elif saque:
                atualizar_dados_conta(contas, conta)
                mensagem = "\r\n" + " Operação bem sucedida. ".center(30, "=")
                mensagem += "\n" + f" Seu saldo é de R$ {conta.saldo:.2f} ".center(30, "=")
            else:
                mensagem = "\r\tNão foi possível realizar a operação."
        except TypeError:
            mensagem = "\r\tEntrada inválida."
        except NameError:
            mensagem = "\r\tVocê precisa entrar com sua conta."

    #  ====================== Mostrar Histórico  ===========================
    elif opcao == 8:
        try:
            conta.historico
        except Exception:
            mensagem = "\r\tVocê precisa entrar com sua conta."

    #  ========================= Finalizar ==============================
    elif opcao == 9:
        print("\nObrigado por utilizar nossos serviços!!!")
        break

    input("\nPressione enter para continuar...")
    abrir_sessao(mensagem)

if hasattr(conta, "limite"):
    contas[str(conta.numero)]["limite"] = conta.limite
    contas[str(conta.numero)]["limite_saque"] = conta.limite_saque
contas[str(conta.numero)]["saldo"] = conta.saldo

with open('./dados/contas.json', 'w') as file:
    file.write(json.dumps(contas))
