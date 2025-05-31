from createdb import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class PedidoItem(Base):
    __tablename__ = "pedido_itens"
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("itens.id"), primary_key=True)
    quantidade = Column(Integer, default=1)

    pedido = relationship("Pedido", back_populates="itens_assoc", overlaps="itens")
    item = relationship("Item", back_populates="pedidos_assoc", overlaps="pedidos")


    # deve ter um init pra essa tabela n pra n ?
