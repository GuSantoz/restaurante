from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from createdb import Base

class Item(Base):
    __tablename__ = "itens"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    valor = Column(Numeric, nullable=False)

    pedidos_assoc = relationship("PedidoItem", back_populates="item")
    pedidos = relationship(
    "Pedido", 
    secondary="pedido_itens", 
    back_populates="itens", 
    overlaps="pedidos_assoc,itens_assoc,pedido"
)

    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor
    