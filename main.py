from classes.funcionario import Funcionario
from classes.garcom import Garcom
from classes.cozinheiro import Cozinheiro
from classes.mesa import Mesa
from classes.item import Item
from classes.pedidoItem import PedidoItem
from classes.pedido import Pedido
from database import *


# Listar mesas
def listar_mesas():
    try:
        mesas = session.query(Mesa).all()
        if not mesas:
            raise ValueError("Não há mesas cadastradas.")
        for mesa in mesas:
            print(f"ID: {mesa.id} | Capacidade: {mesa.capacidade} | Status: {'Ocupada' if mesa.status else 'Livre'} | Atendida por: {mesa.garcom.nome if mesa.garcom else 'Nenhum garçom'} | Conta: R${mesa.conta:.2f}")
    except ValueError as e:
        print(e)
        return "Erro"
    except Exception as e:
        print(f"\nErro inesperado ao listar mesas: {str(e)}")
        return "Erro"

def add_mesa():
    try:
        capacidade = input("Capacidade da mesa: ")
        if not capacidade:
            raise ValueError("A capacidade não pode estar vazia.")
        
        capacidade = int(capacidade)
        if capacidade <= 0:
            raise ValueError("A capacidade deve ser maior que zero.")
            
        mesa = Mesa(capacidade=capacidade)
        session.add(mesa)
        session.commit()
        print("Mesa adicionada com sucesso.")
    except ValueError as e:
        print(f"Erro de valor inválido: {str(e)}")
    except Exception as e:
        print(f"Erro ao adicionar mesa: {str(e)}")

# Atualizar mesa
def update_mesa():
    try:
        if listar_mesas() == "Erro":
            return
        id_ = input("ID da mesa: ")
        if not id_.strip():
            raise ValueError("O ID da mesa não pode estar vazio.")
        id_ = int(id_)
        if id_ <= 0:
            raise ValueError("O ID da mesa deve ser maior que zero.")

        mesa = session.query(Mesa).get(id_)
        if not mesa:
            raise ValueError("Mesa não encontrada.")

        capacidade = input(f"Nova capacidade (atual: {mesa.capacidade}): ")
        try:
            if not capacidade.strip():
                print("Achou")
                raise ValueError
            capacidade = int(capacidade)
            if capacidade <= 0:
                raise ValueError("A capacidade deve ser maior que zero.")
            mesa.capacidade = capacidade
            session.commit()
            print("Mesa atualizada com sucesso.")
        except ValueError:
            raise ValueError("A capacidade deve ser um número inteiro válido.")
    except ValueError as e:
        print(f"Erro: {str(e)}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")

# Deletar mesa
def delete_mesa():
    try:
        if listar_mesas() == "Erro":
            return
        id_ = input("ID da mesa: ")
        if not id_.strip():
            raise ValueError("O ID da mesa não pode estar vazio.")
        id_ = int(id_)
        if id_ <= 0:
            raise ValueError("O ID da mesa deve ser maior que zero.")

        mesa = session.query(Mesa).get(id_)
        if not mesa:
            raise ValueError("Mesa não encontrada.")
            
        session.delete(mesa)
        session.commit()
        print("Mesa deletada com sucesso.")
    except ValueError as e:
        print(f"Erro: {str(e)}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")

def fechar_mesa():
    try:
        if listar_mesas() == "Erro":
            return
        mesa_id = input("ID da mesa: ")
        if  not mesa_id.strip():
            raise ValueError("O ID não pode estar vazio")
        mesa_id = int(mesa_id)
        mesa = session.query(Mesa).get(mesa_id)
        if not mesa:
            raise ValueError("Mesa não encontrada.")
            # return
        if not mesa.pedidos:
            raise ValueError("Não há pedidos para fechar a conta.")
            # return
        
        # Perguntar sobre gorjeta
        gorjeta = input("Gorjeta? (s/n): ").lower() == 's'

        if gorjeta and mesa.garcom:
            mesa.gorjeta = True
            valor_gorjeta = mesa.calcular_gorjeta()
            mesa.garcom.bonus += round(float(valor_gorjeta), 2)
            print(f"Gorjeta de R${valor_gorjeta:.2f} adicionada ao bônus do garçom.")
        
        # Deletar pedidos
        for p in mesa.pedidos:
            session.delete(p)
        
        print(f"Conta da mesa {mesa.id} fechada.")
        if gorjeta:
            print(f"Bônus atual do garçom {mesa.garcom.nome}: R${mesa.garcom.bonus:.2f}")

        # Resetar estado da mesa
        mesa.set_status(False)
        mesa.conta = 0
        mesa.gorjeta = False
        mesa.garcom = None
    except ValueError as e:
        print(f"Erro: {str(e)}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")

    session.commit()

def add_item():
    try:
        nome = input("Nome do item: ")
        if not nome.strip():
            raise ValueError("O nome do item não pode estar vazio.")
            
        valor_input = input("Valor: ")
        if not valor_input.strip():
            raise ValueError("O valor não pode estar vazio.")
            
        try:
            valor = float(valor_input.replace(",", "."))
            if valor <= 0:
                raise ValueError("O valor deve ser maior que zero.")
        except ValueError:
            raise ValueError("O valor deve ser um número válido.")
            
        item = Item(nome=nome, valor=valor)
        session.add(item)
        session.commit()
        print("Item adicionado com sucesso.")
    except ValueError as e:
        print(f"Erro: {str(e)}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")

def listar_itens():
    try:
        item = session.query(Item).all()
        if not item:
            raise ValueError("Não há itens cadastrados.")
        for i in item:
            print(f"ID: {i.id} | Nome: {i.nome} | Valor: R${i.valor:.2f}")
    except ValueError as e:
        print(e)
        return "Erro"

def update_item():
    try:
        listar_itens()
        id_ = input("ID do item: ")
        if not id_.strip():
            raise ValueError("O ID do item não pode estar vazio.")
        id_ = int(id_)
        if id_ <= 0:
            raise ValueError("O ID do item deve ser maior que zero.")

        item = session.query(Item).get(id_)
        if not item:
            raise ValueError("Item não encontrado.")

        nome = input(f"Novo nome (atual: {item.nome}): ")
        if nome.strip():
            item.nome = nome

        valor = input(f"Novo valor (atual: {item.valor:.2f}): ")
        if valor.strip():
            try:
                novo_valor = float(valor.replace(",", "."))
                if novo_valor <= 0:
                    raise ValueError("O valor deve ser maior que zero.")
                item.valor = novo_valor
            except ValueError:
                raise ValueError("O valor deve ser um número válido.")

        session.commit()
        print("Item atualizado com sucesso.")
    except ValueError as e:
        print(f"Erro: {str(e)}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")

def delete_item():
    try:
        listar_itens()
        id_ = input("ID do item: ")
        if not id_.strip():
            raise ValueError("O ID do item não pode estar vazio.")
        id_ = int(id_)
        if id_ <= 0:
            raise ValueError("O ID do item deve ser maior que zero.")

        item = session.query(Item).get(id_)
        if not item:
            raise ValueError("Item não encontrado.")
            
        session.delete(item)
        session.commit()
        print("Item deletado com sucesso.")
    except ValueError as e:
        print(f"Erro: {str(e)}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")

def criar_pedido():
    try:
        if listar_mesas() == "Erro":
            return
        mesa_id = input("ID da mesa: ")
        if not mesa_id.strip():
            raise ValueError("O ID da mesa não pode estar vazio.")
        
        mesa = session.query(Mesa).get(mesa_id)

        if not mesa:
            raise ValueError("Mesa não encontrada.")
        mesa_id = int(mesa_id)
        if mesa_id <= 0:
            raise ValueError("O ID da mesa deve ser maior que zero.")
        

        if not mesa.status:
            if listar_garcons() == "Erro":
                return
            garcom_id = input("Qual garçom está atendendo a mesa? ")
            if not garcom_id.strip():
                raise ValueError("O ID do garçom não pode estar vazio.")
            garcom_id = int(garcom_id)
            if garcom_id <= 0:
                raise ValueError("O ID do garçom deve ser maior que zero.")
            
            garcom = session.query(Garcom).get(garcom_id)
            if not garcom:
                raise ValueError("Garçom não encontrado.")
            mesa.garcom = garcom
            mesa.set_status(True)

        pedido = Pedido(mesa=mesa)
        mesa.adicionar_pedidos(pedido)
        session.add(pedido)
        session.commit()
        print("Pedido criado com sucesso.")
        
    except ValueError as e:
        print(f"Erro: {str(e)}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")

def listar_pedidos():
    pedidos = session.query(Pedido).all()
    if not pedidos:
        print("Não há pedidos cadastrados.")
        return
    for p in pedidos:
        print(f"Pedido {p.id} | Mesa {p.mesa_id} | Total: R${p.total:.2f}")

def adicionar_item_pedido():
    pedidos = session.query(Pedido).all()
    if not pedidos:
        print("Não há pedidos cadastrados.")
        return
    listar_pedidos()
    pedido_id = int(input("ID do pedido: "))
    pedido = session.query(Pedido).get(pedido_id)
    if not pedido:
        print("Pedido não encontrado.")
        return
    if listar_itens() == "Erro":
        return
    item_id = int(input("ID do item: "))
    item = session.query(Item).get(item_id)
    if not item:
        print("Item não encontrado.")
        return
    quantidade = int(input("Quantidade: "))
    assoc = PedidoItem(pedido=pedido, item=item, quantidade=quantidade)
    valor_total = item.valor * quantidade
    pedido.total += valor_total
    
    # Atualizar a conta da mesa
    mesa = pedido.mesa
    if mesa:
        mesa.conta += float(valor_total)
    
    session.add(assoc)
    session.commit()
    print("Item adicionado ao pedido.")
    if mesa:
        print(f"Conta da mesa {mesa.id} atualizada para R${mesa.conta:.2f}")

def cancelar_pedido():
    listar_pedidos()
    pedido_id = int(input("ID do pedido para cancelar: "))
    pedido = session.query(Pedido).get(pedido_id)
    
    if not pedido:
        print("Pedido não encontrado.")
        return
    
    mesa = pedido.mesa
    if mesa:
        mesa.conta -= float(pedido.total)
        if mesa.conta < 0: 
            mesa.conta = 0
        if not mesa.pedidos or len(mesa.pedidos) <= 1:
            mesa.set_status(False)
    else:
        print("Mesa não encontrada.")
    
   
    session.delete(pedido)
    session.commit()
    
    print("Pedido cancelado.")
    if mesa:
        print(f"Conta da mesa {mesa.id} atualizada para R${mesa.conta:.2f}")

def contar_pedidos():
    print(f'O total de pedidos é: {Pedido.contar_pedidos()}')

def add_garcom():
    try:
        nome = input("Nome: ")
        if nome == '':
            raise ValueError("É necessario adicionar o nome do garcom.")
        turno = input("Turno: ")
        if turno == '':
            raise ValueError("É necessario adicionar o turno do garcom.")
        __salario = input("Salário: ")
        if __salario == '':
            raise ValueError("O salario não está de acordo com o esperado!")
        bonus = 0
    except ValueError as e:
        print(e)
    else:
        __salario = float(__salario.replace(",", "."))
        bonus = float(bonus)
        g = Garcom(nome=nome, turno=turno, salario=__salario, bonus=bonus)
        session.add(g)
        session.commit()
        print("Garçom adicionado.")

def add_cozinheiro():
    try:
        nome = input("Nome: ")
        if not nome.strip():
            raise ValueError("O nome não pode estar vazio.")

        turno = input("Turno: ")
        if not turno.strip():
            raise ValueError("O turno não pode estar vazio.")

        salario_input = input("Salário: ")
        if not salario_input.strip():
            raise ValueError("O salário não pode estar vazio.")
        try:
            salario = float(salario_input.replace(",", "."))
            if salario <= 0:
                raise ValueError("O salário deve ser maior que zero.")
        except ValueError:
            raise ValueError("O salário deve ser um número válido.")

        especialidade = input("Especialidade: ")
        if not especialidade.strip():
            raise ValueError("A especialidade não pode estar vazia.")

        c = Cozinheiro(nome=nome, turno=turno, salario=salario, especialidade=especialidade)
        session.add(c)
        session.commit()
        print("Cozinheiro adicionado com sucesso.")
    except ValueError as e:
        print(f"Erro: {str(e)}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")

def listar_garcons():
    try:
        garcons = session.query(Funcionario).filter(Funcionario.cargo == "Garcom").all()
        if not garcons:
            raise ValueError("Nenhum garcom encontrado")
        for g in garcons:
            print(f"ID: {g.id} | Nome: {g.nome} | Turno: {g.turno} | Salário: R${g.salario} | Bônus: R${g.bonus}")
    except ValueError as e:
        print(f"Erro inesperado: {str(e)}")
        return "Erro"

def listar_cozinheiros():
    cozinheiros = session.query(Funcionario).filter(Funcionario.cargo == "Cozinheiro").all()
    if not cozinheiros:
        print("Nenhum cozinheiro encontrado.")
        return "Erro"
    for c in cozinheiros:
        print(f"ID: {c.id} | Nome: {c.nome} | Turno: {c.turno} | Salário: R${c.salario} | Especialidade: {c.especialidade}")

def update_garcom():
    try:
        listar_garcons()
        id_garcom = input("ID do garçom: ")
        if not id_garcom.strip():
            raise ValueError("O ID do garçom não pode estar vazio.")
        id_garcom = int(id_garcom)
        if id_garcom <= 0:
            raise ValueError("O ID do garçom deve ser maior que zero.")

        garcom = session.query(Garcom).get(id_garcom)
        if not garcom:
            raise ValueError("Garçom não encontrado.")
        if not isinstance(garcom, Garcom):
            raise ValueError("O funcionário selecionado não é um garçom.")

        nome = input(f"Novo nome ({garcom.nome}): ")
        if nome.strip():
            garcom.nome = nome

        turno = input(f"Novo turno ({garcom.turno}): ")
        if turno.strip():
            garcom.turno = turno

        salario = input(f"Novo salário (R${garcom.salario:.2f}): ")
        if salario.strip():
            try:
                novo_salario = float(salario.replace(",", "."))
                if novo_salario <= 0:
                    raise ValueError("O salário deve ser maior que zero.")
                garcom.salario = novo_salario
            except ValueError:
                raise ValueError("O salário deve ser um número válido.")

        bonus = input(f"Novo bônus (R${garcom.bonus:.2f}): ")
        if bonus.strip():
            try:
                novo_bonus = float(bonus.replace(",", "."))
                if novo_bonus < 0:
                    raise ValueError("O bônus não pode ser negativo.")
                garcom.bonus = novo_bonus
            except ValueError:
                raise ValueError("O bônus deve ser um número válido.")

        session.commit()
        print("Garçom atualizado com sucesso.")
    except ValueError as e:
        print(f"Erro: {str(e)}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")

def update_cozinheiro():
    try:
        listar_cozinheiros()
        id_cozinheiro = input("ID do cozinheiro: ")
        if not id_cozinheiro.strip():
            raise ValueError("O ID do cozinheiro não pode estar vazio.")
        id_cozinheiro = int(id_cozinheiro)
        if id_cozinheiro <= 0:
            raise ValueError("O ID do cozinheiro deve ser maior que zero.")

        cozinheiro = session.query(Cozinheiro).get(id_cozinheiro)
        if not cozinheiro:
            raise ValueError("Cozinheiro não encontrado.")
        if not isinstance(cozinheiro, Cozinheiro):
            raise ValueError("O funcionário selecionado não é um cozinheiro.")

        nome = input(f"Novo nome ({cozinheiro.nome}): ")
        if nome.strip():
            cozinheiro.nome = nome

        turno = input(f"Novo turno ({cozinheiro.turno}): ")
        if turno.strip():
            cozinheiro.turno = turno

        salario = input(f"Novo salário (R${cozinheiro.salario:.2f}): ")
        if salario.strip():
            try:
                novo_salario = float(salario.replace(",", "."))
                if novo_salario <= 0:
                    raise ValueError("O salário deve ser maior que zero.")
                cozinheiro.salario = novo_salario
            except ValueError:
                raise ValueError("O salário deve ser um número válido.")

        especialidade = input(f"Nova especialidade ({cozinheiro.especialidade}): ")
        if especialidade.strip():
            cozinheiro.especialidade = especialidade

        session.commit()
        print("Cozinheiro atualizado com sucesso.")
    except ValueError as e:
        print(f"Erro: {str(e)}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")

def delete_garcom():
    try:
        if listar_garcons() == "Erro":
            return
        id_funcionario = input("ID do funcionário: ")
        if not id_funcionario.strip():
            raise ValueError("O ID do funcionário não pode estar vazio.")
        id_funcionario = int(id_funcionario)
        if id_funcionario <= 0:
            raise ValueError("O ID do funcionário deve ser maior que zero.")
        
        f = session.query(Funcionario).get(id_funcionario)
        if not f:
            raise ValueError("Funcionário não encontrado.")
        
        garcom = session.query(Garcom).get(id_funcionario)
        if not garcom:
            raise ValueError("O funcionário não é um Garçom, então não pode ser deletado.")
            
        session.delete(f)
        session.commit()
        print("Funcionário deletado com sucesso.")
    except ValueError as e:
        print(f"Erro: {str(e)}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")

def delete_cozinheiro():
    try:
        if listar_cozinheiros() == "Erro":
            return
        id_funcionario = input("ID do funcionário: ")
        if not id_funcionario.strip():
            raise ValueError("O ID do funcionário não pode estar vazio.")
        id_funcionario = int(id_funcionario)
        if id_funcionario <= 0:
            raise ValueError("O ID do funcionário deve ser maior que zero.")

        f = session.query(Funcionario).get(id_funcionario)
        if not f:
            raise ValueError("Funcionário não encontrado.")
       
        cozinheiro = session.query(Cozinheiro).get(id_funcionario)
        if not cozinheiro:
            raise ValueError("O funcionário não é um Cozinheiro, então não pode ser deletado.")
            
        session.delete(f)
        session.commit()
        print("Funcionário deletado com sucesso.")
    except ValueError as e:
        print(f"Erro: {str(e)}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")

# Separando menus

def menu_mesa():
    options = {
        '1': listar_mesas,
        '2': add_mesa,
        '3': update_mesa, 
        '4': delete_mesa,
        '5': fechar_mesa
        # '6': 
        # '7':
        # '8':

    }

    while True:
        print("\n[ MENU MESA ]")
        print("1. Listar Mesas")
        print("2. Adicionar Mesa")
        print("3. Atualizar Mesa")
        print("4. Deletar Mesa")
        print("5. Fechar Conta da Mesa")
        print("6. Voltar")


        op = input("Escolha: ")
        if op == '6':
            break 
        action = options.get(op)
        if action:
            action()
        else:
            print("Opção inválida.")


def menu_item():
    options = {
        '1': listar_itens, 
        '2': add_item,
        '3': adicionar_item_pedido,
        '4': update_item, 
        '5': delete_item
    }

    while True:
        print("\n[ MENU ITEM ]")
        print("1. Listar Itens")
        print("2. Adicionar Item")
        print("3. Adicionar item ao pedido")
        print("4. Atualizar Item")
        print("5. Deletar Item")
        print("6. Voltar")


        op = input("Escolha: ")
        if op == '6':
            break 
        action = options.get(op)
        if action:
            action()
        else:
            print("Opção inválida.")


def menu_pedido():
    options = {
        '1': listar_pedidos, 
        '2': criar_pedido,
        '3': adicionar_item_pedido,
        '4': cancelar_pedido,
        '5': contar_pedidos
    }

    while True:
        print("\n[ MENU PEDIDO ]")
        print("1. Listar Pedidos")
        print("2. Adicionar Pedido")
        print("3. Adicionar Item ao Pedido")
        print("4. Cancelar Pedido")
        print("5. Exibir Total Pedidos")
        print("6. Voltar")


        op = input("Escolha: ")
        if op == '6':
            break 
        action = options.get(op)
        if action:
            action()
        else:
            print("Opção inválida.")

def menu_garcom():
    options = {
        '1': listar_garcons,
        '2': add_garcom,
        '3': update_garcom,
        '4': delete_garcom, 
        # '5': delete_item
    }
        
    while True:
        print("\n[ MENU GARÇOM ]")
        print("1. Listar Garçons")
        print("2. Adicionar Garçom")
        print("3. Atualizar Garçom")
        print("4. Deletar Garçom")
        print("5. Voltar")

        op = input("Escolha: ")
        if op == '5':
            break 
        action = options.get(op)
        if action:
            action()
        else:
            print("Opção inválida.")

def menu_cozinheiro():
    options = {
        '1': listar_cozinheiros, 
        '2': add_cozinheiro,
        '3': update_cozinheiro,
        '4': delete_cozinheiro, 
        # '5': delete_item
    }

    while True:
        print("\n[ MENU COZINHEIRO ]")
        print("1. Listar Cozinheiros")
        print("2. Adicionar Cozinheiro")
        print("3. Atualizar Cozinheiro")
        print("4. Deletar Cozinheiro")
        print("5. Voltar")


        op = input("Escolha: ")
        if op == '5':
            break 
        action = options.get(op)
        if action:
            action()
        else:
            print("Opção inválida.")

def menu():
    options = {
        '1': menu_mesa,
        '2': menu_item,
        '3': menu_pedido,
        '4': menu_garcom,
        '5': menu_cozinheiro
    }

    while True:
        print("\n[ MENU RESTAURANTE ]")
        print("1. MENU MESA")
        print("2. MENU ITEM")
        print("3. MENU PEDIDO")
        print("4. MENU GARÇOM")
        print("5. MENU COZINHEIRO")
        print("6. Sair")

        op = input("Escolha: ")
        if op == '6':
            break
        action = options.get(op)
        if action:
            action()
        else:
            print("Opção inválida.")

if __name__ == '__main__':
    menu()
