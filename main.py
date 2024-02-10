import textwrap


def menu() -> str:
    display = """\n
    =============== MENU ===============
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(display))


def depositar(saldo_d: float, valor_d: float, extrato_d: str, /) -> tuple:
    if valor_d > 0:
        saldo_d += valor_d
        extrato_d += f"Depósito: R$ {valor_d:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo_d, extrato_d


def sacar(*, saldo_s: float, valor_s: float, extrato_s: float, limite_s: float,
          numero_saques_s: int, limite_saque_s: int) -> tuple:

    excedeu_saldo = valor_s > saldo_s
    excedeu_limite = valor_s > limite_s
    excedeu_saques = numero_saques_s >= limite_saque_s

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor_s > 0:
        saldo_s -= valor_s
        extrato_s += f"Saque: R$ {valor_s:.2f}\n"
        numero_saques_s += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo_s, extrato_s, numero_saques_s


def exibir_extrato(saldo_e: float, /, *, extrato_e: float) -> None:
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato_e else extrato_e)
    print(f"\nSaldo: R$ {saldo_e:.2f}")
    print("==========================================")


def criar_usuario(usuarios: list) -> None:
    cpf = input("Informe o CPF (Somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usu;ario com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade" +
                     "/sigla estado: ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento,
                     "cpf": cpf, "endereco": endereco})

    print("\n=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf: str, usuarios: list) -> list:
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia: str, numero_conta: int, usuarios: list) -> dict:
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta,
                "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrada! @@@")
    return {}


def listar_contas(contas):
    if contas:
        for conta in contas:
            linha = f"""
                Agência:\t{conta['agencia']}
                C/C:\t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']}
            """
            print("." * 100)
            print(textwrap.dedent(linha))
    else:
        print("\n@@@ Nenhum usuário cadastrado! @@@")


def main() -> None:
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo_s=saldo,
                valor_s=valor,
                extrato_s=extrato,
                limite_s=limite,
                numero_saques_s=numero_saques,
                limite_saque_s=LIMITE_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato_e=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == "lc":
            listar_contas(contas)
        
        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == '__main__':
    main()
    
