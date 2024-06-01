# Otimização de Sistema Bancário DIO com POO

Desafio de Otimização da 2ª versão do Sistema Bancário DIO usando funções Python, agora usando Programação Orientada a Objetos (POO)

A primeira versão do projeto pode ser acessada [aqui](https://github.com/ju-c-lopes/sistema-bancario-dio).

A segunda versão utilizando funções pode ser acessada [aqui](https://github.com/ju-c-lopes/sistema-bancario-dio-com-funcoes/tree/main)

---

## Requisitos

---

### Objetivos Gerais

---

#### Definir as funcionalidades existentes em classes Python POO:

<cliente.py>
1. classe Pessoa Física
    * Atributos privados
        - CPF
        - nome
        - data de nascimento
    
    * métodos
        - construtor
        - __new__
        * propriedades
            - cpf
            - nome
            - data de nascimento
        - validar cpf
        - validar data de nascimento

2. classe Cliente, sendo uma subclasse de Pessoa Fisica
    * Atributos privados
        - lista de contas
        - endereço

    * método estático
        - checar clientes
    
    * métodos de classe
        - construtor
        - definir endereço
        - validar endereço
        * propriedades
            - contas
            - endereço
        - adicionar conta

<conta.py>
1. classe Conta
    * atributos privados
        - agencia
        - número 
        - saldo
        - cliente (cpf da classe Cliente)
        - histórico

    * métodos
        * propriedades
            - saldo
            - número 
            - histórico
        - construtor
        - nova conta
        - sacar
        - depositar

2. classe ContaCorrente, sendo uma subclasse de Conta
    * atributos privados
        - limite
        - limite de saque

    * métodos
        - construtor
        - nova conta
        * propriedades
            - limite
            - limite de saque
        - sacar

<historico.py>
1. classe Historico
    * atributos privados
        - número
        - histórico

    * métodos
        - construtor
        - adicionar transação
        * propriedades
            - histórico

<transacao.py>
1. classe abstrata transacao
    * método abstrato
        - registrar

2. classe Deposito, sendo uma subclasse de Transacao
    * método registrar, que recebe os seguintes parâmetros:
        - conta (instância de Conta ou ContaCorrente)
        - valor depositado

3. classe Saque, sendo uma subclasse de Transacao
    * método registrar, que recebe os seguintes parâmetros:
        - conta (instância de Conta ou ContaCorrente)
        - valor sacado

---

A aplicação do projeto é administrada no arquivo <code>operaco_bancaria.py</code> funcionando de maneira semelhante a segunda versão, porém utilizando das funcionalidades da **Programação Orientada a Objetos**.

Os dados estão sendo persistidos nos arquivos <code>./dados/clientes.json</code> e <code>./dados/contas.json</code>, assim como os históricos de operações para cada conta que estão sendo salvos em arquivos exclusivos para cada conta no formato <code>conta_<nroconta>.txt</code>.

* OBS: como o propósito é a prática da **Programação Orientada a Objetos** e a persistência dos dados não foi um requisito de prática, escolhi essa abordagem afim de praticar outras maneiras de persistência de dados, porém, há formas muito mais seguras e eficientes de persistência, como banco de dados.