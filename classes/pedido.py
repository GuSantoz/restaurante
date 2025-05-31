from .mesa import Mesa
from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from createdb import Base
from database import Session

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True)
    mesa_id = Column(Integer, ForeignKey("mesas.id"))
    total = Column(Numeric, default=0)

    mesa = relationship("Mesa", back_populates="pedidos")
    itens_assoc = relationship("PedidoItem", back_populates="pedido", cascade="all, delete-orphan")
    itens = relationship(
    "Item", 
    secondary="pedido_itens", 
    back_populates="pedidos", 
    overlaps="itens_assoc,pedidos_assoc,item"
)

    def __init__(self, mesa: Mesa, total = 0):
        self.mesa = mesa
        # self.itens = [] 
        self.total = total
        self.mesa.adicionar_pedidos(self)
        Pedido.contar_pedidos()

    @classmethod
    def contar_pedidos(cls):
        session = Session()
        try:
            return session.query(cls).count()
        finally:
            session.close()

    def get_total(self):
        return self.total
    
    def adicionar_item(self, item):
        self.itens.append(item)

    def calcular_total(self):
        for item in self.itens:
            self.total += item.valor
    