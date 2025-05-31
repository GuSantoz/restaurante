# from pedido import Pedido
from sqlalchemy import Column, ForeignKey, Integer, Float, Boolean
from sqlalchemy.orm import relationship
from createdb import Base

class Mesa(Base):
    __tablename__ = "mesas"
    id = Column(Integer, primary_key=True)
    capacidade = Column(Integer)
    status = Column(Boolean, default=False)
    gorjeta = Column(Boolean, default=False)
    conta = Column(Float, default=0.0)

    pedidos = relationship("Pedido", back_populates="mesa")

    garcom_id = Column(Integer, ForeignKey('garcons.id'))
    garcom = relationship("Garcom", back_populates="mesas")

    def __init__(self, capacidade, status = False, gorjeta = False, conta = 0):
        self.capacidade = capacidade
        self.status = status
        self.gorjeta = gorjeta
        # self.pedidos = []
        self.conta = conta

        
    def adicionar_pedidos(self, pedido):
        self.pedidos.append(pedido)
        valor = pedido.get_total()
        self.conta += float(valor)
        
    def set_status(self, status):
        self.status = status

    def get_conta(self):
        return self.conta

    def calcular_gorjeta(self, percentual=0.1):
        return self.conta * percentual
    
