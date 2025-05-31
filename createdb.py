from database import Base, db

# ... importar todas as classes que criam tabelas

def criar_tabelas():
    print("Iniciando criação de tabelas...")
    from classes.funcionario import Funcionario
    from classes.garcom import Garcom
    from classes.cozinheiro import Cozinheiro
    from classes.mesa import Mesa
    from classes.item import Item
    from classes.pedidoItem import PedidoItem
    from classes.pedido import Pedido
    Base.metadata.create_all(bind=db)

if __name__ == "__main__":
    criar_tabelas()
    print("Tabelas criadas com sucesso.")